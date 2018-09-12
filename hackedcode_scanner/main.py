'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from importlib import import_module
import logging
import os
import argparse
from pathlib import Path
from pkg_resources import resource_filename
from .lib.helpers import load_yaml

MODULE_NAME = "hackedcode_scanner"


def parse_args():
    """Opts parser function."""
    parser = argparse.ArgumentParser(
        description="""Scan app project and find hints of possible hacking""")

    parser.add_argument("-c", "--config", nargs=1, required=False,
                              help='''path of a configuration yaml file''',
                              type=str)

    parser.add_argument("-l", "--level", required=False,
                              default="warning",
                              help='''level of output''',
                              type=str)

    parser.add_argument("path",
                        help='''Path of the root of the app's project''',
                        type=str, nargs=1)

    return parser.parse_args()


def main():
    """Main function. Manage CLI client"""

    args = parse_args()
    level = args.level
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        level=getattr(logging, level.upper()),
                        handlers=[logging.StreamHandler()])

    # get default config installed with package
    default_config = resource_filename(MODULE_NAME, 'config/config.yml')

    if args.config:
        CONFIG = load_yaml(args.config[0])
    else:
        CONFIG = load_yaml(default_config)

    if CONFIG["log_enabled"]:
        logging.getLogger().addHandler(logging.FileHandler(CONFIG["log_path"]))
    logging.debug("Yaml config loaded")

    # adquire the valid full path of project path
    project_path = str(Path(args.path[0]).resolve())

    # load plugins
    plugins_loaded = []
    for plugin in CONFIG['plugins_enabled']:
        try:
            plugins_loaded.append(import_module(
                '{}.plugins.{}'.format(MODULE_NAME, plugin)))
            plugins_loaded[-1].name = plugin
            logging.debug("plugin {} loaded".format(plugin))
        except ImportError as e:
            logging.warning("can't load {} plugin: {}".format(plugin, e.msg))
    logging.debug("Plugins loaded")

    # Run scanner
    logging.info("Begin scan")
    for plugin in plugins_loaded:
        try:
            os.chdir(project_path)
            plugin.run_plugin(config=CONFIG["plugin_config"][plugin.name])
        except KeyError as e1:
            raise("probably the config file has errors.", e1)
        except Exception as e2:
            raise(e2)
            logging.critical("Execution of plugin {} fail: {}".format(
                plugin.name, e2))
    logging.info("Scan finished")


if __name__ == '__main__':
    main()

from importlib import import_module
import logging
import os
from concurrent.futures import ProcessPoolExecutor as executor


class PluginError(Exception):
    """Standard exception to report errors to the plugin caller."""

    pass


def load_configfile(path='config.yml'):
    """
    Read and load YAML config file.

    :param path: filepath of yaml configfile
    :type path: str
    :return: yaml content
    :rtype: dict
    """
    try:
        import yaml
    except ImportError as e:
        print(e, "A error ocurred when trying to use the pyyaml library. "
              "This library must be installed to use this program. "
              "You can try with 'pip install pyyaml' command")
        raise SystemExit
    try:
        with open(path, 'r') as file:
            config = yaml.load(file)
        return config
    except Exception as e:
        raise(e)
global test
test = "jasjs"

def main():
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        filename='drwatcher.log', level=logging.INFO)
    CONFIG = load_configfile()
    logging.info("Yaml config loaded")
    project_path = "."  # must be an argument script
    plugins_loaded = []
    logging.info("Begin scan")
    for plugin in CONFIG['plugins_enabled']:
        try:
            plugins_loaded.append(import_module('plugins.{}'.format(plugin)))
            plugins_loaded[-1].name = plugin
        except ImportError as e:
            logging.warning("can't load {} plugin: {}".format(plugin, e.msg))
    for plugin in plugins_loaded:
        try:
            plugin.run_plugin(project_path=project_path,
                              config=CONFIG["plugin_config"][plugin.name],
                              verbose=False)
        except Exception as e:
            logging.critical("Execution of plugin {} fail: {}".format(plugin.name, e))
        logging.info("Scan finished")

if __name__ == '__main__':
    main()

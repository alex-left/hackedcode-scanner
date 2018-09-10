from importlib import import_module
import logging
import os
import argparse


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
        logging.error("""A error ocurred when trying to use the pyyaml library.
              This library must be installed to use this program.
              You can try with 'pip install pyyaml' command {}""".format(e))
        raise SystemExit
    try:
        with open(path, 'r') as file:
            config = yaml.load(file)
        return config
    except Exception as e:
        raise(e)


def parse_args():
    """Opts parser function."""
    parser = argparse.ArgumentParser(
        description="""Scan app project and find hints of possible hacking""")

    parser.add_argument("-c", "--config", nargs=1, required=False,
                              help='''path of a config.yml file''', type=str)

    parser.add_argument("path",
                        help='''root path of the app''',
                        type=str, nargs=1)

    return parser.parse_args()


def main():
    """Main function."""

    args = parse_args()
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        level=logging.INFO,
                        handlers=[logging.StreamHandler()])
    if args.config:
        CONFIG = load_configfile(args.config)
    else:
        CONFIG = load_configfile()
    if CONFIG["log_enabled"]:
        logging.getLogger().addHandler(logging.FileHandler(CONFIG["log_path"]))
    logging.info("Yaml config loaded")
    project_path = args.path[0]
    plugins_loaded = []
    for plugin in CONFIG['plugins_enabled']:
        try:
            plugins_loaded.append(import_module('plugins.{}'.format(plugin)))
            plugins_loaded[-1].name = plugin
            logging.info("Plugin {} loaded".format(plugin))
        except ImportError as e:
            logging.warning("can't load {} plugin: {}".format(plugin, e.msg))
    logging.info("Plugins loaded")
    logging.info("Begin scan")
    os.chdir(project_path)
    for plugin in plugins_loaded:
        try:
            plugin.run_plugin(config=CONFIG["plugin_config"][plugin.name],
                              verbose=False)
        except KeyError as e1:
            raise("probably the config file has errors.", e1)
        except Exception as e2:
            raise(e2)
            logging.critical("Execution of plugin {} fail: {}".format(
                plugin.name, e2))
    logging.info("Scan finished")


if __name__ == '__main__':
    main()

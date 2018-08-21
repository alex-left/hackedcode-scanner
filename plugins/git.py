from functools import partial
from subprocess import check_output
from fnmatch import fnmatch
import logging

def run_plugin(project_path, config, verbose):
    """
    Run git status command in project and parse not committed files.
    If the files not are excluded, report them.

    :param project_path: absolut path of the git project
    :type project_path: str
    :param config: plugin config defined in config.yml
    :type config: dict
    """
    excluded_files = config["excluded_files"]
    msg = "GIT - found not expected file: {}"
    try:
        status = check_output(["git", "-C", project_path,
                               "status", "--porcelain"]).decode().splitlines()
    except Exception as e:
        raise(PluginError(e))

    files = (line[3:] for line in status)

    for file in files:
        check_exclude = partial(fnmatch, file)
        if not any(map(check_exclude, excluded_files)):
            logging.info(msg.format(file))
            print(msg.format(file))


class PluginError(Exception):
    """Standard exception to report errors to the plugin caller."""

    pass

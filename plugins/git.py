"""
Run git status command in project path and parse not committed files.
If the files not are excluded, report them.
"""

from functools import partial
from subprocess import check_output
from fnmatch import fnmatch
import logging


def run_plugin(config, verbose):
    """
    :param config: plugin config defined in yaml
    :type config: dict
    """
    excluded_files = config["excluded_files"]
    msg = "GIT - found not expected file: {}"
    try:
        status = check_output(["git", "status",
                                "--porcelain"]).decode().splitlines()
    except Exception as e:
        raise(e)

    files = (line[3:] for line in status)

    for file in files:
        check_exclude = partial(fnmatch, file)
        if not any(map(check_exclude, excluded_files)):
            logging.info(msg.format(file))

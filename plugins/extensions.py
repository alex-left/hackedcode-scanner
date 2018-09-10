"""
Examine all files in project_path defined in config file
and report all files which have the defined extensions.
"""


from pathlib import Path
from fnmatch import fnmatch
import logging
from functools import partial
import os


def run_plugin(config, verbose=False):
    """
    :param config: plugin config defined in config.yml
    :type config: dict
    :param verbose: report if verbose mode is enabled, false by default
    :type verbose: bolean
    """

    def check_path(work_path):
        for root, dirs, files in os.walk(str(work_path)):
            root = Path(root)
            paths = (root / file for file in files)
            for item in paths:
                check_exclude = partial(fnmatch, str(item))
                results = [item for extension in target_extensions if (
                    item.is_file() and
                    not any(map(check_exclude, excluded_paths)) and
                    extension in item.suffixes)]
                if results:
                    msg = \
                        "EXTENSIONS - found file: {}".format(
                            item.resolve())
                    logging.info(msg)

    target_paths = config["target_paths"]
    target_extensions = config["target_extensions"]
    excluded_paths = config["excluded_paths"]

    for target_path in target_paths:
        work_path = Path(target_path)
        if work_path.exists() and work_path.is_dir():
            check_path(work_path)

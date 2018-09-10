"""
Examine all files in project_path, exclude files defined as glob patterns in
config file and check if have execution permission.
"""

import logging
from lib.helpers import filter_files


def run_plugin(config, *args, **kwargs):
    """
    :param config: plugin config defined in yaml
    :type config: dict
    """
    excluded_files = config["excluded_files"]
    paths = filter_files(excluded_files)
    for item in paths:
            logging.debug("analizing {}".format(item))
        if item.is_file():
            check_file(item)


def check_file(filepath):
    """
    Check execution perms of single file.
    :param filepath: Path object with file to examine
    :type filepath: pathlib.Path
    """
    # read mode in decimal, convert it to string binary and choose last 9
    # bits corresponding to user, group and other permisssions
    perms = bin(filepath.stat().st_mode)[-9:]

    # check the bits correnponding to execution: rw(X)rw(X)rw(X)
    for bit in perms[2::3]:
        if bool(int(bit)):
            msg_perm = "PERMS - found execution perms in file: {}\n".format(
                filepath.resolve())
            logging.warning(msg_perm)
            break

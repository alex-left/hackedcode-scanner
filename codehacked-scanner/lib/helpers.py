"""Useful functions for plugins."""

from pathlib import Path
from glob import glob
import os


def filter_files(excluded_files):
    """
    Scan all files into current path, filter then and returns a generator
    of all valid paths in order with excluded files.
    :param excluded_files: names (glob supported) of the files to exclude
    :type excluded_files: list of strings
    :return: generator of pathlib.Path items
    """
    excluded_items = []
    # generate a list with result of globbing
    for result in map(glob, excluded_files):
        excluded_items.extend([Path(item) for item in result])

    for root, dirs, files in os.walk(os.getcwd()):
        root = Path(root)
        for file in files:
            # this is necessary because the glob module is not recursive.
            # The expected result is like the git program: if the pattern
            # have not a wildcard, apply to all subpaths.
            if (
                not any(filter(
                    lambda x: x in str(root) + "/", excluded_files)
                    ) and
                    root / file not in excluded_items):
                yield root / file

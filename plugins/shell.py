"""
Examine all files in project_path, exclude files defined as glob patterns in
config file and analyze the content of each file searching for strings that
indicates possible and forbbiden shell code.
"""

import logging
import re
from lib.helpers import filter_files
from concurrent.futures import ProcessPoolExecutor


def run_plugin(config, verbose=False):
    """
    :param config: plugin config defined in yaml
    :type config: dict
    :param verbose: report if verbose mode is enabled, false by default
    :type verbose: bolean
    """

    excluded_files = config["excluded_files"]
    pattern = re.compile('|'.join(pat for pat in config["patterns"]))
    paths = filter_files(excluded_files)
    executor = ProcessPoolExecutor()
    for item in paths:
        if item.is_file():
            executor.submit(check_file, pattern, item)


def check_file(pattern, path):
    """
    Analyze content of single file.

    :param pattern: regex pattern
    :type pattern: str
    :param path: Path object with file to examine
    :type path: pathlib.Path
    """
    content = path.read_text(encoding='utf-8', errors='ignore')
    for result in re.finditer(pattern, content):
        if result:
            msg_content = \
                "SHELL - found suspect string in file: {}\nLINE: {}".format(
                    path.resolve(), result.group())
            logging.info(msg_content)

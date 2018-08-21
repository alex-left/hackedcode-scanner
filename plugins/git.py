import logging

def run_plugin(project_path, CONFIG):
    from subprocess import check_output
    from fnmatch import fnmatch

    project_path = kwargs["project_path"]
    excluded_files = CONFIG["excluded_files"]

    status = check_output(["git", "-C", project_path,
                           "status", "-s"]).decode().splitlines()]

    files = [file.split(" ")[1] for file in status]
    files = [file for file in files if not ]

    msg = "found not expected file: {}"

    for file in files:
        if file not in excluded_files and not fnmatch:
            print(msg.format(file))
            logging.info(msg.format(file))

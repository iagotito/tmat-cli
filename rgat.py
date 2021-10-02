"""Redmine and Github Automation Tool (RGAT)

Usage:
    rgat.py config
    rgat.py redmine create <file>

Options:
    -h --help  Show this screen.
    --version  Show version.

"""
import os
import getpass

import yaml

from modules.docopt import docopt
from modules import redmine


def create_config_file():
    config = {}
    config["project-url"] = input("Project url: ")
    # TODO: use api key to avoid write login info in a file
    config["username"] = input("Usarname: ")
    config["password"] = getpass.getpass("Password: ")

    with open("config.yaml", "w") as f:
        yaml.dump(config, stream=f, sort_keys=False)


def main():
    arguments = docopt(__doc__, version="RGAT 0.1")

    if arguments.get("config"):
        create_config_file()

    elif arguments.get("redmine"):
        if arguments.get("create"):
            filepath = os.path.abspath(str(arguments.get("<file>")))
            config_path = os.path.abspath("./config.yaml")
            try:
                redmine.create(filepath, config_path)
            except AssertionError as e:
                print(str(e))


if __name__ == '__main__':
    main()

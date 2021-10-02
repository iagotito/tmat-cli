"""Redmine and Github Automation Tool (RGAT)

Usage:
    rgat.py config

Options:
    -h --help  Show this screen.
    --version  Show version.

"""
import getpass

import yaml

from modules.docopt import docopt


def create_config_file():
    config = {}
    config["project_url"] = input("Project url: ")
    # TODO: use api key to avoid write login info in a file
    config["username"] = input("Usarname: ")
    config["password"] = getpass.getpass("Password: ")

    with open("config.yaml", "w") as f:
        yaml.dump(config, stream=f, sort_keys=False)


def main():
    arguments = docopt(__doc__, version="RGAT 0.1")

    if arguments.get("config"):
        create_config_file()


if __name__ == '__main__':
    main()

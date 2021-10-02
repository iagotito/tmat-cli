"""Redmine and Github Automation Tool (RGAT)

Usage:
    rgat.py config

Options:
    -h --help  Show this screen.
    --version  Show version.

"""
from modules.docopt import docopt


def main():
    arguments = docopt(__doc__, version="RGAT 0.1")
    print(arguments)


if __name__ == '__main__':
    main()

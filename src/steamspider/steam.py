#! /usr/local/bin/python3

from menu import Menu
import json
from sys import argv


def init_config():
    with open('./config-files/db.json') as db_file, \
            open('./config-files/process.json') as work_file:
        db_config = json.load(db_file)
        work_config = json.load(work_file)

    return db_config, work_config


def main(argv):
    db_config, work_config = init_config()
    menu = Menu(db_config, work_config, argv)
    menu.execute()


if __name__ == '__main__':
    main(argv)

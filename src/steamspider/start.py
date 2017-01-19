#! /usr/bin/python3

from workerpool import WorkerPool
import json


def start():
    with open('./config-files/db.json') as db_file, \
            open('./config-files/process.json') as work_file:
        db_config = json.load(db_file)
        work_config = json.load(work_file)
    pool = WorkerPool(work_config, db_config)
    pool.start()


if __name__ == '__main__':
    start()

#! /usr/bin/python3

import pymysql
import json


def init_db(config_file_path):
    with open(config_file_path) as config_file:
        db_config = json.load(config_file)

    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['username'],
        db=db_config['database'],
        password=db_config['password'])

    with connection.cursor() as cursor, open('tables.sql') as sql_file:
        cursor.execute(sql_file.read())
    connection.commit()


if __name__ == '__main__':
    init_db('../config-files/db.json')

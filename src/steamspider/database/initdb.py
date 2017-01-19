# /usr/bin/env python3

import pymysql
import json

if __name__ == '__main__':
    with open('db.json') as config_file:
        db_config = json.load(config_file)

    connection = pymysql.connect(
        host='localhost',
        user=db_config['user'],
        db=db_config['database'],
        password=db_config['password'])

    with connection.cursor() as cursor, open('tables.sql') as sql_file:
        cursor.execute(sql_file.read())
    connection.commit()

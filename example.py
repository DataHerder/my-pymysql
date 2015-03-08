#!/usr/bin/python

from Sql.Sql import Sql

localhost = True


# change per your development flavor: configurable
# wrapper function for pymysql.connect must return
# object of key value pairs
def parameters(pymysql):
    if localhost is True:
        return {
            'host': 'localhost',
            'user': 'root',
            'passwd': '[your-password]',
            'db': '[your-computer-db]',
            'cursorclass': pymysql.cursors.DictCursor
        }
    else:
        return {
            'host': 'localhost',
            'user': 'root',
            'passwd': '[your-password-on-server]',
            'db': '[your-db-name-on-server]',
            'cursorclass': pymysql.cursors.DictCursor
        }

sql = Sql(_init=parameters).select()
print sql.table('test').fields('*').where(1)
print sql.all()

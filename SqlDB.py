#!/usr/bin/python
import pymysql
import SqlSelect


class SqlDB(SqlSelect.SqlSelect):
    def __init__(self, **kwargs):
        self._cursor = None
        if kwargs['_init'] is not None:
            db_conn = kwargs['_init'](pymysql)
            self._conn(**db_conn)
        else:
            self._conn(**kwargs)
        self._pymysql = pymysql
        super(SqlDB, self).__init__()

    def _conn(self, **kwargs):
        self._conn_ = pymysql.connect(**kwargs)
        self._cursor = self._conn_.cursor()

    def _exec(self, sql=""):
        self._cursor.execute(sql, self._prepare_vars)
        return self._cursor
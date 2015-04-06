#!/usr/bin/python

import SqlSelect


class SqlSelect(SqlSelect):

    def __init__(self):
        # super(object, self).__init_()
        """init function"""
        super(SqlSelect, self).__init__()

    def __getattr__(self, name):

        def wrapper(*args):
            if name is 'innerJoin':
                self.join_type = 'inner'
                return self.join(*args)
            elif name is 'outerJoin':
                self.join_type = 'outer'
                return self.join(*args)
            elif name is 'naturalJoin':
                self.join_type = 'natural'
                return self.join(*args)
            elif name is 'leftJoin':
                self.join_type = 'left'
                return self.join(*args)
            elif name is 'rightJoin':
                self.join_type = 'right'
                return self.join(*args)
            else:
                # object.__getattribute__(self, name)
                raise AttributeError(name + ' is not supported')

        return wrapper

    def join(self, *args):
        """join"""
        elements = args[2]
        on_data = []
        for key in elements:
            on_data.append('`' + key + '`.`' + elements[key] + '`')

        self._joins.append("""%s JOIN %s AS %s ON %s = %s""" %
                           (self.join_type.upper(), args[0], args[1], on_data[0], on_data[1]))
        # print "\n".join(self._joins)
        return self

    def all(self):
        sql = self._compile()
        cursor = self._exec(sql)
        rows = []

        for row in cursor:
            rows.append(row)

        return rows


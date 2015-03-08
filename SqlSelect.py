#!/usr/bin/python

class SqlSelect(object):

    def __init__(self):
        # super(object, self).__init_()
        """init function"""
        self.join_type = None
        self._tables = []
        self._fields = {}
        self._where = "1"
        self._joins = []
        self._limit = None
        self._raw_where = '1'
        self._prepare_vars = []
        super(SqlSelect, self).__init__()


    def reset(self):
        """
        Duplicate code?
        :return: self
        """
        self.join_type = None
        self._tables = []
        self._fields = {}
        self._where = "1"
        self._joins = []
        self._limit = None
        self._raw_where = '1'
        self._prepare_vars = []
        return self

    def table(self, table_name=None, alias='a'):
        if table_name is None:
            return self

        self._tables.append({'alias': alias, 'table_name': table_name})
        return self

    def fields(self, *fields):
        if type(fields[0]) is dict:
            # what we have here is that the first element is a dictionary
            for key in fields[0]:
                if type(fields[0][key]) is list or type(fields[0][key]) is tuple:
                    self._fields[key] = fields[0][key]
                else:
                    if key not in self._fields:
                        self._fields[key] = []
                        self._fields[key].append(fields[0][key])
                    else:
                        self._fields[key].append(fields[0][key])
        elif type(fields[0]) is str:
            self._fields['a'] = []
            for key in fields:
                self._fields['a'].append(key)

        else:
            raise ValueError('Sql.select.fields does not support ' + type(fields[0]))

        return self

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

    def where(self, where_statement = '1', variables=[]):
        """join"""
        for index in range(len(variables)):
            variables[index] = self._pymysql.escape_string(str(variables[index]))

        self._raw_where = where_statement
        self._prepare_vars = tuple(variables)
        return self

    def limit(self, num=0):
        self._limit = 'LIMIT '+str(num)
        return self

    def all(self):
        sql = self._compile()
        cursor = self._exec(sql)
        rows = []

        for row in cursor:
            rows.append(row)

        return rows

    def _compile(self, keep_vars_separate = True):
        # initial select
        sql = "SELECT\n"
        __fields__ = []
        for alias in self._fields:
            for key in self._fields[alias]:
                __fields__.append("\t`"+alias+"`.`"+key+"`")
        sql += ",\n".join(__fields__)+"\n"

        # from statement
        sql += "FROM\n"
        __tables__ = []
        for key in self._tables:
            __tables__.append("\t"+'`'+key['table_name']+'` AS `' + key['alias'] + '`')
        sql += ",\n".join(__tables__)+"\n"

        # joins statement
        for key in self._joins:
            sql += key+"\n"

        # where statement
        sql += "WHERE "
        if keep_vars_separate is True:
            sql += self._raw_where
        else:
            sql += "(" + str(self._raw_where) % self._prepare_vars + ")\n"
        # group by
        # having
        # order by
        # limit
        if self._limit is not None:
            sql += self._limit

        return sql
import pymysql


class MySQLConn(object):
    def __init__(self, db_data):
        """
        :param db_data: dict of database data
        """
        self.conn = pymysql.connect(host=db_data['host'], user=db_data['user'], password=db_data['password'],
                                    port=db_data['port'], db=db_data['database'])

    def create_table(self, sql):
        """
        :param sql: Executable SQL statement
        :return: None
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print('create table error: ', e.args)
            self.conn.rollback()

    def insert(self, data, table):
        """
        :param data: the data needed insert
        :param table: the databese table needed insert
        :return: None
        """
        if not data:
            print('the data needed insert is None')
            return None

        cursor = self.conn.cursor()

        # data is a SQL statement
        if isinstance(data, str):
            try:
                cursor.execute(data)
                self.conn.commit()
            except Exception as e:
                print('insert error: ', e.args)
                self.conn.rollback()
        # data is a dict
        else:
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            sql = 'INSERT INTO {table}({keys}) VALUES({values})'.format(table=table, keys=keys, values=values)
            try:
                if cursor.execute(sql, tuple(data.values())):
                    print('insert success\n')
                    self.conn.commit()
            except Exception as e:
                print('insert failed: ', e.args)
                self.conn.rollback()

    def select(self, sql):
        """
        :param sql: Executable SQL statement
        :return: the result tuple
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            # every time return 50 rows
            rows = cursor.fetchmany(5)
            while rows:
                yield rows
                rows = cursor.fetchmany(50)
        except Exception as e:
            print('select error: ', e.args)

    def update(self, data, table):
        """
        :param data: data need update
        :param table: data needed update
        :return: None
        """
        if not data:
            print('the data needed update is None')
            return None

        cursor = self.conn.cursor()

        # data is a SQL statement
        if isinstance(data, str):
            try:
                cursor.execute(data)
                self.conn.commit()
            except Exception as e:
                print('update error: ', e.args)
                self.conn.rollback()
        # data is a dict
        else:
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            sql = 'INSERT INTO {table}({keys}) VALUES({values}) ON DUPLICATE KEY UPDATE ' \
                .format(table=table, keys=keys, values=values)
            updates = ', '.join(["{key} = %s".format(key=key) for key in data])
            sql += updates
            try:
                if cursor.execute(sql, tuple(data.values()) * 2):
                    self.conn.commit()
            except Exception as e:
                print('update error:', e.args)
                self.conn.rollback()

    def delete(self, sql):
        """
        :param sql: Executable SQL statement
        :return: None
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print('delete error: ', e.args)
            self.conn.rollback()

    def __del__(self):
        self.conn.close()


class MongoDBConn(object):
    pass


class RedisConn(object):
    pass
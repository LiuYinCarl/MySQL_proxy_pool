import pymysql


class MySQL_conn:
    def __init__(self, host, user, passwd, port, db):
        self.conn = pymysql.connect(host=host, user=user, password=passwd, port=port, db=db)

    def create_table(self, sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print('create table error: ', e)
            self.conn.rollback()

    def insert(self, data, table):
        if not data:
            print('the data needed insert is None')
            return None

        cursor = self.conn.cursor()
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES({values})'.format(table=table, keys=keys, values=values)
        try:
            if cursor.execute(sql, tuple(data.values())):
                print('insert success\n')
                self.conn.commit()
        except Exception as e:
            print('insert failed: ', e)
            self.conn.rollback()

    def select(self, sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            # try yield and fetchone to overwrite
            return cursor.fetchall()
        except Exception as e:
            print('select error: ', e)

    def update(self, data, table):
        if not data:
            print('the data needed update is None')
            return None

        cursor = self.conn.cursor()
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
            print('update error:', e)
            self.conn.rollback()

    def delete(self, sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print('delete error: ', e)
            self.conn.rollback()

    def __del__(self):
        self.conn.close()

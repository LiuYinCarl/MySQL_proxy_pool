class MySQLConfig(object):
    def __init__(self):
        """
        initial MySQL configuration data
        """
        self.host = 'localhost'
        self.user = 'root'
        self.password = '7873215'
        self.port = 3306
        self.database = 'proxies'

    def check_config(self):
        """
        check the config data prevent setting errors
        :return: None
        """
        if not self.host:
            print('your MySQL host no setting')
        if not self.user:
            print('your MySQL user no setting')
        if not self.password:
            print('your MySQL password no setting')
        if not self.port:
            print('your MySQL port no setting')
        if not self.database:
            print('your MySQL database no setting')

    def get_data(self):
        """
        :return: dict of MySQL configuration data
        """
        self.check_config()
        db_data = {'host': self.host,
                   'user': self.user,
                   'password': self.password,
                   'port': self.port,
                   'database': self.database
                   }
        return db_data

    def set_data(self, data):
        """
        :param data: a dict of MySQL configuration data such as
        {'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'port': 3306
        'database': 'db'
        }
        :return: None
        """
        submit_errors = 0
        if 'host' not in data.keys:
            print('submit config data have not host')
            submit_errors += 1
        if 'user' not in data.keys:
            print('submit config data have not user')
            submit_errors += 1
        if 'password' not in data.keys:
            print('submit config data have not password')
            submit_errors += 1
        if 'port' not in data.keys:
            print('submit config data have not port')
            submit_errors += 1
            if 'database' not in data.keys:
                print('submit config data have not database')
                submit_errors += 1

        if not submit_errors:
            self.host = data['host']
            self.user = data['user']
            self.password = data['password']
            self.port = data['port']
            self.database = data['database']
        else:
            print('the submit data have %s error, submission failed' % submit_errors)


class MongoDBConfig(object):
    pass


class RedisCongig(object):
    pass


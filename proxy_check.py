import aiohttp
import asyncio
import time
from db_conn import MySQLConn
from db_config import MySQLConfig

TEST_URL = 'http://www.baidu.com'
VALID_STATUS_CODES = [200]


class MySQLProxyCheck(object):

    def __init__(self):
        db = MySQLConfig().get_data()
        self.conn = MySQLConn(db)

    async def __test_http_proxy(self, proxy, table):
        """
        test single http proxy
        :param proxy: single http proxy such as ('106.56.102.53', '808')
        :param table: database table need test
        :return:
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                http_proxy = 'http://' + proxy[0] + ':' + proxy[1]
                async with session.get(TEST_URL, proxy=http_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        print("%s is available" % proxy[0])
                        sql = "UPDATE %s SET score = score-10 WHERE ip = '%s'" % (table, proxy[0])
                        self.conn.update(sql, None)
                    else:
                        print("%s is unavailable" % proxy[0])
                        sql = "UPDATE %s SET score = score-10 WHERE ip = '%s'" % (table, proxy[0])
                        self.conn.update(sql, None)
            except Exception as e:
                sql = "UPDATE %s SET score = score-10 WHERE ip = '%s'" % (table, proxy[0])
                self.conn.update(sql, None)
                print('proxy request error: ', e.args)

    async def __test_https_proxy(self, proxy, table):
        """
        test single https proxy
        :param proxy: single https proxy
        :param table: database table need test
        :return:
        """
        pass

    async def __test_socks4_5_proxy(self, proxy, table):
        """
        test single socks4/5 proxy
        :param proxy: single socks4/5 proxy
        :param table: database table need test
        :return:
        """
        pass

    def run_test_http_proxy(self, table):
        """
        :return: None
        """
        sql = "SELECT ip, port FROM {0} WHERE protocol = 'HTTP'".format(table)
        try:
            for proxies in self.conn.select(sql):
                proxies = list(proxies)
                print(proxies)
                loop = asyncio.get_event_loop()
                # for i in range(0, 100, BATCH_TEST_SIZE):
                # test_proxys = [proxy for proxy in proxies[i: i + BATCH_TEST_SIZE]]
                tasks = [self.__test_http_proxy(proxy, table) for proxy in proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('Tester error: ', e.args)

    def run_test_https_proxy(self, table):
        pass

    def run_test_socks4_5_proxy(self, table):
        pass


class MongoDBProxyCheck(object):
    pass


class RedisProxyCheck(object):
    pass

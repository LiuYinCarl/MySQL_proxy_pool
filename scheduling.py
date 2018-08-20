from proxy_check import MySQLProxyCheck
from crawl_proxies import Crawl


class MySQLProxyPool(object):

    def run_MySQL_pool(self):
        table = 'xici'

        # xici = Crawl()
        # xici.run_crawl_xici(table)
        check = MySQLProxyCheck()
        check.run_test_http_proxy(table)


class MongoDBProxyPool(object):
    pass


class RedisProxyPool(object):
    pass


if __name__ == '__main__':
    MySQL_pool_test = MySQLProxyPool()
    MySQL_pool_test.run_MySQL_pool()

import requests
import re
from db_conn import MySQLConn
from db_config import MySQLConfig
import time


class Crawl(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(HTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }

    def __crawl_xici(self):
        """
        获取西刺代理
        """
        url = 'http://www.xicidaili.com/nn/'
        for i in range(1, 50):
            real_url = url + str(i)
            try:
                time.sleep(5)
                response = requests.get(real_url, headers=self.headers)
                if response.status_code == 200:
                    pattern_1 = re.compile('(<tr.*?</tr>)', re.S)
                    pattern_2 = re.compile('<td>(.*?)</td>', re.S)
                    results = re.findall(pattern_1, response.text)
                    for result in results:
                        elements = re.findall(pattern_2, result)
                        if elements:
                            print([elements[0], elements[1], elements[3]])
                            yield elements[0], elements[1], elements[3]
            except ConnectionError as e:
                print('Connection Error', e.args)

    def run_crawl_xici(self, table):
        db = MySQLConfig().get_data()
        conn = MySQLConn(db)
        # if you want to continue crawl proxies, instead it by "while True"
        while True:
            try:
                for items in self.__crawl_xici():
                    data = {'ip': items[0],
                            'port': items[1],
                            'protocol': items[2],
                            'score': 100
                            }
                    conn.update(data, table)
            except Exception as e:
                print('cycle error: ', e.args)
                pass
            # every 10 minutes crawl once
            time.sleep(600)

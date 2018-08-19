import requests
import re
import MySQL_conn
import time


def crawl_XiCi():
    """
    获取西刺代理
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(HTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    url = 'http://www.xicidaili.com/'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pattern_1 = re.compile('(<tr.*?</tr>)', re.S)
            pattern_2 = re.compile('<td>(.*?)</td>', re.S)
            results = re.findall(pattern_1, response.text)
            for result in results:
                elements = re.findall(pattern_2, result)
                if not elements == []:
                    print(':'.join([elements[0], elements[1], elements[2], elements[3]]))
                    yield elements[0], elements[1], elements[2], elements[3]
    except ConnectionError as e:
        print('Connection Error', e.args)


if __name__ == '__main__':

    host = 'localhost'
    user = 'root'
    passwd = '7873215'
    port = 3306
    databese = 'proxies'
    table = 'xici'

    db = MySQL_conn.MySQL_conn(host, user, passwd, port, databese)
    while True:
        try:
            for items in crawl_XiCi():
                data = {'ip': items[0],
                        'port': int(items[1]),
                        'protocol': items[2],
                        'position': items[3]
                        }
                db.update(data, table)
        except Exception as e:
            print('cycle error: ', e)
            pass
        # every 10 minutes cycle one time
        time.sleep(600)

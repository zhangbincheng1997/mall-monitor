from bs4 import BeautifulSoup  # pip install beautifulsoup4
import execjs  # pip install PyExecJS
import requests
import json
import time


class Crawl:
    def __init__(self, js_file='MMM_GET_TOKEN.js'):
        content = ''
        with open(js_file, 'r') as f:
            for line in f.readlines():
                content += line
        self.js = execjs.compile(content)
        self.API = 'http://tool.manmanbuy.com/history.aspx?DA=1&action=gethistory&url=%s&bjid=&spbh=&cxid=&zkid=&w=951&token=%s'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }

    def get(self, id):
        return self.get_name(id), self.get_price(id), int(time.time())

    def get_name(self, id):
        url = 'https://item.jd.com/%s.html' % id
        try:
            response = requests.get(url, headers=self.headers)
            if response.text:
                soup = BeautifulSoup(response.text, 'html.parser')
                name = soup.find(class_='sku-name')
                return name.text.strip()
        except Exception as e:
            print(e)
            return

    def get_price(self, id):
        url = 'https://p.3.cn/prices/mgets?skuIds=%s' % id
        try:
            response = requests.get(url, headers=self.headers)
            if response.text:
                data = json.loads(response.text)
                return float(data[0]['p'])
        except Exception as e:
            print(e)
            return

    def get_history(self, id):
        url = 'https://item.jd.com/%s.html' % id
        token = self.js.call('d.encrypt', url, '2', 'true')
        api = self.API % (url, token)
        try:
            response = requests.get(api, headers=self.headers)
            if response.text:
                data = json.loads(response.text)
                history = eval('[' + data['datePrice'] + ']')
                datePrice = {}
                datePrice['date'] = []
                datePrice['price'] = []
                datePrice['msg'] = []
                for h in history:
                    date = time.strftime('%Y-%m-%d', time.localtime(h[0] / 1000))
                    datePrice['date'].append(date)
                    datePrice['price'].append(h[1])
                    datePrice['msg'].append(h[2])
                return datePrice
        except Exception as e:
            print(e)
            return


if __name__ == '__main__':
    crawl = Crawl()
    print(crawl.get('4311178'))
    print(crawl.get_history('https://item.jd.com/4311178.html'))

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

    def get(self, id):
        return self.get_name(id), self.get_price(id), int(time.time())

    # 获取商品名称
    def get_name(self, id):
        url = 'https://item.jd.com/%s.html' % id
        retry_count = 5  # 重传机制
        while retry_count > 0:
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                name = soup.find(class_='sku-name')
                return name.text.strip()
            except Exception as e:
                retry_count -= 1
                print(e)
        return None

    # 获取当前价格
    def get_price(self, id):
        url = 'https://p.3.cn/prices/mgets?skuIds=%s' % id
        retry_count = 5  # 重传机制
        while retry_count > 0:
            try:
                # 使用代理
                response = requests.get(url)
                data = json.loads(response.text)
                return float(data[0]['p'])
            except Exception as e:
                retry_count -= 1
                print(e)
        return None

    # 获取历史价格
    def get_history(self, id):
        url = 'https://item.jd.com/%s.html' % id
        token = self.js.call('d.encrypt', url, '2', 'true')
        api = self.API % (url, token)
        retry_count = 5  # 重传机制
        while retry_count > 0:
            try:
                response = requests.get(api)
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
                retry_count -= 1
                print(e)
        return None


if __name__ == '__main__':
    crawl = Crawl()
    print(crawl.get('4311178'))
    print(crawl.get_history('https://item.jd.com/4311178.html'))

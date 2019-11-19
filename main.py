from selenium import webdriver
from goods import Goods
import threading
import time


class Monitor():
    def __init__(self, inc, ids):
        options = webdriver.ChromeOptions()
        options.headless = True  # 无界面模式
        self.driver = webdriver.Chrome(options=options)
        self.inc = inc
        self.ids = ids
        self.goodsDict = {}

    # 爬虫任务
    def task(self):
        for id in self.ids:
            url = 'https://item.jd.com/%d.html' % id
            self.driver.get(url)

            # 商品名称
            name = self.driver.find_element_by_class_name('sku-name').text
            # 商品价格
            price = self.driver.find_element_by_class_name('J-p-' + str(id)).text
            # 记录时间
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            if id not in self.goodsDict.keys():
                want = price
                self.goodsDict[id] = Goods(id, want, name, price, date)
            else:
                self.goodsDict[id].add(price, date)

            time.sleep(1)

        # https://www.echartsjs.com/examples/zh/editor.html?c=line-simple
        for goods in self.goodsDict.values():
            goods.out()
        print('----------')

    # 周期性定时器
    def run(self):
        self.task()
        timer = threading.Timer(self.inc, self.run)  # delay function
        timer.start()


if __name__ == '__main__':
    inc = 10
    ids = ['4311178', '4311182', '100002795959', '100004751037', '8797490']
    monitor = Monitor(inc, ids)
    monitor.run()

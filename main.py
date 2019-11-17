from selenium import webdriver
from goods import Goods
import threading
import time

ids = [4311178, 100002795959]
goodsDict = {}
driver = webdriver.Chrome()
inc = 10


# 爬虫任务
def task():
    for id in ids:
        url = 'https://item.jd.com/%d.html' % id
        driver.get(url)

        # 商品名称
        name = driver.find_element_by_class_name('sku-name').text
        # 商品价格
        price = driver.find_element_by_class_name('J-p-' + str(id)).text
        # 记录时间
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        if id not in goodsDict.keys():
            goodsDict[id] = Goods(url, name, price, date)
        else:
            goodsDict[id].add(price, date)

        time.sleep(1)

    # https://www.echartsjs.com/examples/zh/editor.html?c=line-simple
    for goods in goodsDict.values():
        goods.out()
    print('----------')


# 周期性定时器
def monitor():
    task()
    timer = threading.Timer(inc, monitor)  # delay function
    timer.start()


if __name__ == '__main__':
    monitor()

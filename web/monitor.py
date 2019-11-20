from selenium import webdriver
from goods import Goods
import threading
import time


class Monitor():
    def __init__(self, email='1656704949@qq.com', rate=60):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 关闭界面
        options.add_argument('--no-sandbox')  # 关闭沙箱
        prefs = {
            'profile.managed_default_content_settings': {
                'images': 2,  # 不加载图片
                # "User-Agent": ua,  # 更换UA
            }}
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)
        self.driver2 = webdriver.Chrome(options=options)
        self.rate = rate  # 刷新频率
        self.email = email  # 电子邮箱
        self.goodsDict = {}

    # 新增商品
    def add(self, id, want):
        if id not in self.goodsDict.keys():
            name, price, date = self.crawl(id, self.driver2)
            self.goodsDict[id] = Goods(id, want, name, price, date)
            return True
        else:
            return False

    # 删除商品
    def remove(self, id):
        if id in self.goodsDict.keys():
            self.goodsDict.pop(id)
            return True
        else:
            return False

    # 设置参数
    def setting(self, email, rate):
        self.email = email
        self.rate = rate

    def crawl(self, id, driver):
        # 电脑 https://item.jd.com/xxxx.html
        # 手机 https://item.m.jd.com/product/xxxx.html
        url = 'https://item.jd.com/%s.html' % id
        driver.get(url)
        # 商品名称
        name = driver.find_element_by_class_name('sku-name').text
        # 当前价格
        price = driver.find_element_by_class_name('J-p-' + id).text
        # 记录时间
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return name, price, date

    # 定时任务
    def task(self):
        ids = list(self.goodsDict.keys())
        for id in ids:
            if self.goodsDict[id].status == '1':
                name, price, date = self.crawl(id, self.driver)
                self.goodsDict[id].update(name, price, date)
                time.sleep(1)  # 休息一下
        # TEST
        for goods in self.goodsDict.values():
            goods.out()

    # 定时器
    def run(self):
        self.task()
        timer = threading.Timer(self.rate, self.run)  # delay function
        timer.start()


if __name__ == '__main__':
    ids = ['4311178', '4311182', '100002795959', '100004751037', '8797490']
    wants = [219.00, 339.00, 4900.00, 5600.00, 8998.00]

    monitor = Monitor(rate=10)
    for id, want in zip(ids, wants):
        monitor.add(id, want)
    monitor.run()

from selenium import webdriver
from goods import Goods
from db import DB
from mail import Mail
import threading
import time


class Monitor:
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
        self.goods_dict = {}
        self.db = DB()
        self.mail = Mail()
        self.email = email  # 电子邮箱
        self.rate = rate  # 刷新频率

        # 加载数据
        result = self.db.query()
        print('----------加载数据----------')
        for id, item in result.items():
            goods = Goods(item['id'], item['want'], item['status'], item['history_price'], item['history_date'])
            self.goods_dict[id] = goods
            print(goods.__dict__)
        print('----------加载完成----------')

    # 添加商品
    def add(self, id, want, status=True):
        if id not in self.goods_dict.keys():
            self.goods_dict[id] = Goods(id, want, status, [], [])
            self.db.add(id, want, status)
            return True
        else:
            return False

    # 删除商品
    def remove(self, id):
        if id in self.goods_dict.keys():
            self.goods_dict.pop(id)
            self.db.delete(id)
            return True
        else:
            return False

    # 更新期望价格
    def update_want(self, id, want):
        if id in self.goods_dict.keys():
            self.goods_dict[id].update_want(want)
            self.goods_dict[id].update_note(0)
            self.db.update_want(id, want)
            return True
        else:
            return False

    # 更新运行状态
    def update_status(self, id, status):
        if id in self.goods_dict.keys():
            self.goods_dict[id].update_status(status)
            self.goods_dict[id].update_note(0)
            self.db.update_status(id, status)
            return True
        else:
            return False

    # 爬取商品
    def crawl(self, url, driver):
        # 爬取链接
        driver.get(url)
        # 商品名称
        name = driver.find_element_by_class_name('sku-name').text
        # 当前价格 'J-p-' + id
        price = float(driver.find_element_by_css_selector('.p-price > .price').text)
        # 记录时间
        date = int(time.time())  # time.strftime('%Y-%m-%d %H:%M:%S', time.time())
        return name, price, date

    # 定时任务
    def task(self):
        ids = list(self.goods_dict.keys())
        for id in ids:
            goods = self.goods_dict[id]
            if goods.status:
                # 电脑 https://item.jd.com/xxxx.html
                # 手机 https://item.m.jd.com/product/xxxx.html
                url = 'https://item.jd.com/%s.html' % id
                name, price, date = self.crawl(url, self.driver)
                if id not in self.goods_dict.keys(): continue  # 防止商品已经删除
                goods.update(name, price, date)

                ########## 检查是否需要保存历史 ##########
                zerotime = time.strftime('%Y-%m-%d %H:00:00', time.localtime(date))  # 当前整点字符串
                # zerotime = time.strftime('%Y-%m-%d %0:00:00', time.localtime(date))  # 当天零点字符串
                zerotime = int(time.mktime(time.strptime(zerotime, '%Y-%m-%d %H:%M:%S')))  # 字符串转时间戳
                # 添加历史
                if len(goods.history_date) == 0 or goods.history_date[-1] != zerotime:
                    goods.add_history(price=price, date=zerotime)
                    self.db.add_history(id, price=price, date=zerotime)
                # 修改历史
                elif price != goods.history_price[-1]:
                    goods.update_history(price=price, date=zerotime)
                    self.db.update_history(id, price=price, date=zerotime)

                ########## 检查是否符合发送条件 ##########
                NOTE = 60 * 60  # 一小时
                # NOTE = 60 * 60 * 24 # 一天
                # 满足通知间隔时间 & 当前价格小于期望价格
                if (date - goods.note >= NOTE) and (price <= goods.want):
                    self.mail.send(self.email, name, price, goods.want,
                                   max(goods.history_price), min(goods.history_price), url)
                    goods.update_note(int(time.time()))
        print('----------刷新数据----------')
        for goods in self.goods_dict.values():
            print(goods.__dict__)
        print('----------刷新完成----------')

    # 定时器
    def _run(self):
        self.task()
        timer = threading.Timer(self.rate, self._run)  # delay function
        timer.start()

    # 定时器
    def run(self):
        timer = threading.Timer(self.rate, self._run)  # delay function
        timer.start()


if __name__ == '__main__':
    ids = ['4311178', '4311182', '100002795959', '100004751037', '8797490']
    wants = [219.00, 339.00, 4900.00, 5600.00, 8998.00]

    monitor = Monitor(rate=10)
    for id, want in zip(ids, wants):
        monitor.add(id, want)
    monitor.run()

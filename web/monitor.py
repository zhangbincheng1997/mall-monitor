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

        # 记录数据
        self.driver = webdriver.Chrome(options=options)  # 添加的时候
        self.driver2 = webdriver.Chrome(options=options)  # 监控的时候
        self.email = email  # 电子邮箱
        self.rate = rate  # 刷新频率
        self.goods_dict = {}  # 商品字典
        self.db = DB()
        self.mail = Mail()

        # 加载数据
        result = self.db.query()
        print('加载数据')
        for id, item in result.items():
            goods = Goods(item['id'], item['want'], item['status'], item['note'],
                          item['history_price'], item['history_date'])
            self.goods_dict[id] = goods
            print(goods.__dict__)

    # 爬取商品
    def crawl(self, id, driver):
        # 电脑 https://item.jd.com/xxxx.html
        # 手机 https://item.m.jd.com/product/xxxx.html
        url = 'https://item.jd.com/%s.html' % id
        driver.get(url)
        # 商品名称
        name = driver.find_element_by_class_name('sku-name').text
        # 当前价格
        price = float(driver.find_element_by_class_name('J-p-' + id).text)
        # 当前时间
        date = int(time.time())  # time.strftime("%Y-%m-%d %H:%M:%S", time.time())
        return name, price, date

    # 添加商品
    def add(self, id, want):
        if id not in self.goods_dict.keys():
            name, price, date = self.crawl(id, self.driver)
            self.goods_dict[id] = Goods(id, want, name, price, date)
            self.db.add(id, want, date, price)
            return True
        else:
            return False

    # 删除商品
    def remove(self, id):
        if id in self.goods_dict.keys():
            self.goods_dict.pop(id)
            self.db.delete_goods(id)
            return True
        else:
            return False

    # 更新期望价格
    def update_want(self, id, want):
        if id in self.goods_dict.keys():
            self.goods_dict[id].update_want(want)
            self.db.update_want(id, want)
            return True
        else:
            return False

    # 更新运行状态
    def update_status(self, id, stauts):
        if id in self.goods_dict.keys():
            self.goods_dict[id].update_status(stauts)
            self.db.update_status(id, stauts)
            return True
        else:
            return False

    # 定时任务
    def task(self):
        ids = list(self.goods_dict.keys())
        for id in ids:
            if self.goods_dict[id].status == 1:
                name, price, date = self.crawl(id, self.driver2)
                # 防止已经被删除
                if id not in self.goods_dict.keys():
                    continue
                # 更新信息
                self.goods_dict[id].update(name, price, date)
                # 更新历史
                self.goods_dict[id].update_history(price=price, date=date)
                self.db.add_history(id, price=price, date=date)
                print(self.goods_dict[id].__dict__)
                # 检查是否符合发送条件
                if self.goods_dict[id].check():
                    self.send_mail(self.goods_dict[id])  # 发送邮件
                    # 更新邮件发送时间
                    note = int(time.time())
                    self.goods_dict[id].update_note(int(time.time()))
                    self.db.update_note(id, note)
                time.sleep(1)  # 休息一下
        # TEST
        for goods in self.goods_dict.values():
            print(goods.__dict__)

    # 定时器
    def run2(self):
        self.task()
        timer = threading.Timer(self.rate, self.run2)  # delay function
        timer.start()

    def run(self):
        timer = threading.Timer(self.rate, self.run2)  # delay function
        timer.start()

    # 发送邮件
    def send_mail(self, goods):
        url = 'https://item.jd.com/%s.html' % goods.id
        high = max(goods.history_price)
        low = min(goods.history_price)
        self.mail.send(self.email, goods.name, goods.want, goods.price, high, low, url)


if __name__ == '__main__':
    ids = ['4311178', '4311182', '100002795959', '100004751037', '8797490']
    wants = [219.00, 339.00, 4900.00, 5600.00, 8998.00]

    monitor = Monitor(rate=10)
    for id, want in zip(ids, wants):
        monitor.add(id, want)
    monitor.run()

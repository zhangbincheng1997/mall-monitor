from db import DB
from crawl import Crawl
from goods import Goods
from mail import Mail
import threading
import time


class Monitor:
    def __init__(self, email='1656704949@qq.com', rate=60):
        self.goods_dict = {}
        self.db = DB()
        self.crawl = Crawl()
        self.mail = Mail()
        self.email = email  # 电子邮箱
        self.rate = rate  # 刷新频率

        # 加载数据
        result = self.db.query()
        print('----------加载数据----------')
        for id, item in result.items():
            name, price, date = self.crawl.get(id)
            self.goods_dict[id] = Goods(item['id'], item['want'], item['status'], name, price, date)
            print(self.goods_dict[id].__dict__)
        print('----------加载完成----------')

    # 添加商品
    def add(self, id, want, status=True):
        if id not in self.goods_dict.keys():
            name, price, date = self.crawl.get(id)
            self.goods_dict[id] = Goods(id, want, status, name, price, date)
            self.db.add(id, want, status)
            print(self.goods_dict[id].__dict__)
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
            self.goods_dict[id].update_note(0)  # 刷新通知时间
            self.db.update_want(id, want)
            return True
        else:
            return False

    # 更新运行状态
    def update_status(self, id, status):
        if id in self.goods_dict.keys():
            self.goods_dict[id].update_status(status)
            self.goods_dict[id].update_note(0)  # 刷新通知时间
            self.db.update_status(id, status)
            return True
        else:
            return False

    # 获取历史价格
    def history(self, id):
        if id in self.goods_dict.keys():
            return self.crawl.get_history(id)
        else:
            return ''

    # 定时任务
    def task(self):
        ids = list(self.goods_dict.keys())
        for id in ids:
            goods = self.goods_dict[id]
            if goods.status:
                name, price, date = self.crawl.get(id)
                if id not in self.goods_dict.keys(): continue  # 防止商品已经删除
                goods.update(name, price, date)

                ########## 检查是否符合发送条件 ##########
                NOTE = 60 * 60  # 一小时
                # NOTE = 60 * 60 * 24 # 一天
                # 满足通知间隔时间 & 当前价格小于期望价格
                if (date - goods.note >= NOTE) and (price <= goods.want):
                    self.mail.send(self.email, name, price, goods.want, goods.url)
                    goods.update_note(date)
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

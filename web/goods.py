class Goods:
    def __init__(self, id, want, status=1, note=0, history_price=[], history_date=[]):
        self.id = id  # 商品编号
        self.want = want  # 期望价格
        self.name = '等待中...'  # 商品名称
        self.price = '-'  # 当前价格
        self.date = 1569859200  # 当前日期 2019-10-01 00:00:00
        self.status = status  # 运行状况
        self.note = note  # 通知备注
        self.history_price = history_price  # 历史价格
        self.history_date = history_date  # 历史日期

    def update(self, name, price, date):
        self.name = name
        self.price = price
        self.date = date

    def update_want(self, want):
        self.want = want

    def update_status(self, status):
        self.status = status

    def update_note(self, note):
        self.note = note

    def update_history(self, price, date):
        self.history_price.append(price)
        self.history_date.append(date)

    def check(self):
        # 距离上次通知超过一小时 60*60 & 当前价格小于期望价格
        return (self.date - self.note >= 3600) and (self.price <= self.want)

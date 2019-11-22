class Goods:
    def __init__(self, id, want, status, history_price, history_date):
        self.id = id  # 商品编号
        self.want = want  # 期望价格
        self.status = status  # 运行状况
        self.name = '等待中...'  # 商品名称
        self.price = '-'  # 当前价格
        self.date = 1569859200  # 记录日期 2019-10-01 00:00:00
        self.note = 0  # 通知备注
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
        self.history_price[-1] = price
        self.history_date[-1] = date

    def add_history(self, price, date):
        self.history_price.append(price)
        self.history_date.append(date)

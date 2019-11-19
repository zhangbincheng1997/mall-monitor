class Goods():
    def __init__(self, id, want, name, price, date):
        self.id = id
        self.want = want
        self.name = name
        self.price = price
        self.date = date
        self.status = '1'
        self.history_price = [price]
        self.history_date = [date]

    def add(self, price, date):
        self.history_price.append(price)
        self.history_date.append(date)

    def change(self, status):
        self.status = status

    def out(self):
        print(self.__dict__)
        # print('\n'.join(['%s:%s' % item for item in self.__dict__.items()]))

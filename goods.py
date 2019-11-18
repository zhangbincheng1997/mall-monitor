class Goods():
    def __init__(self, id, want, name, price, date):
        self.id = id
        self.want = want
        self.name = name
        self.price = price
        self.date = date
        self.history_price = []
        self.history_date = []

    def add(self, price, date):
        self.history_price.append(price)
        self.history_date.append(date)

    def out(self):
        print(self.__dict__)
        # print('\n'.join(['%s:%s' % item for item in self.__dict__.items()]))

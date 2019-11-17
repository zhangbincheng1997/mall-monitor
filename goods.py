class Goods():
    def __init__(self, url, name, price, date):
        self.url = url
        self.name = name
        self.price = [price]
        self.date = [date]

    def add(self, price, date):
        self.price.append(price)
        self.date.append(date)

    def out(self):
        print('\n'.join(['%s:%s' % item for item in self.__dict__.items()]))

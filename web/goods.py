class Goods():
    def __init__(self, id, want, name, price, date):
        self.id = id
        self.want = want
        self.status = '1'
        self.name = name
        self.price = price
        self.date = date
        self.history_price = []
        self.history_date = []

    def update(self, name, price, date):
        self.name = name
        self.price = price
        self.date = date
        if len(self.history_price) == 0 or not self.history_price[-1] == price:
            self.history_price.append(price)
            self.history_date.append(date)

    def change(self, status):
        self.status = status

    def out(self):
        print(self.__dict__)

from sqlalchemy import create_engine, Column, String, FLOAT, Integer, BOOLEAN, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# 建立基本映射类
Base = declarative_base()


# 定义映射类Goods
class Goods(Base):
    __tablename__ = 'goods'
    id = Column(Integer, primary_key=True, autoincrement=True)
    gid = Column(String(20), nullable=False)  # 商品编号
    want = Column(FLOAT, nullable=False)  # 期望价格
    status = Column(Integer, default=1)  # 运行状态
    note = Column(Integer, default=0)  # 通知备注
    history = relationship('History', back_populates='goods')  # 一对多

    def __repr__(self):
        return "<Goods(id=%d, gid='%s', want=%.2f, status=%d, note=%d)>" % \
               (self.id, self.gid, self.want, self.status, self.note)


# 定义映射类History(Child)
class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Integer, nullable=False)  # 历史日期
    price = Column(FLOAT, nullable=False)  # 历史价格
    goods_id = Column(Integer, ForeignKey('goods.id'))  # 外键
    goods = relationship('Goods', back_populates="history")  # 一对多

    def __repr__(self):
        return "<History(id=%d, date=%d, price=%.2f)>" % \
               (self.id, self.date, self.price)


class DB:
    def __init__(self):
        # 创建数据库连接
        engine = create_engine('sqlite:///foo.db?check_same_thread=False', echo=True)  # 任意线程都可使用
        # 创建数据库表格
        Base.metadata.create_all(engine)
        # 创建Session类
        self.session = sessionmaker(bind=engine)()

    def query(self):
        goodss = self.session.query(Goods).all()
        result = {}
        for goods in goodss:
            item = {}
            item['id'] = goods.gid
            item['want'] = goods.want
            item['status'] = goods.status
            item['note'] = goods.note
            item['history_date'] = []
            item['history_price'] = []
            for history in goods.history:
                item['history_date'].append(history.date)
                item['history_price'].append(history.price)
            result[goods.gid] = item
        return result

    def add(self, gid, want, date, price):
        goods = Goods(gid=gid, want=want)
        goods.history = [History(date=date, price=price)]
        self.session.add(goods)
        self.session.commit()

    # Goods -> History -> date price
    def add_history(self, gid, date, price):
        goods = self.session.query(Goods).filter_by(gid=gid).first()
        goods.history.append(History(date=date, price=price))
        self.session.add(goods)
        self.session.commit()

    def update_want(self, gid, want):
        goods = self.session.query(Goods).filter_by(gid=gid).first()
        goods.want = want
        self.session.commit()

    def update_status(self, gid, status):
        goods = self.session.query(Goods).filter_by(gid=gid).first()
        goods.status = status
        self.session.commit()

    def update_note(self, gid, note):
        goods = self.session.query(Goods).filter_by(gid=gid).first()
        goods.note = note
        self.session.commit()

    # Goods -> History -> date price
    def update_history(self, gid, date, price):
        goods = self.session.query(Goods).filter_by(gid=gid).first()
        history = self.session.query(History).filter_by(goods_id=goods.id, date=date).first()
        history.price = price
        self.session.commit()

    def delete_goods(self, gid):
        goods = self.session.query(Goods).filter_by(gid=gid).first()
        self.session.delete(goods)
        self.session.commit()


if __name__ == '__main__':
    db = DB()

    print("添加测试：")
    db.add('4311178', 219.00, 1574352000, 229.00)
    db.add_history('4311178', 1574179200, 249.00)
    db.add_history('4311178', 1574265600, 249.00)
    print(db.query())

    print("修改测试：")
    db.update_want('4311178', 209.00)
    db.update_history('4311178', 1574265600, 239.00)
    db.update_status('4311178', 0)
    db.update_note('4311178', 1574352000)
    print(db.query())

    print("删除测试：")
    db.delete_goods('4311178')
    print(db.query())

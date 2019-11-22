from sqlalchemy import create_engine, Column, String, FLOAT, Integer, BOOLEAN, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# 建立基本映射类
Base = declarative_base()


# 定义映射类Goods
class Goods(Base):
    __tablename__ = 'goods'
    id = Column(String(20), primary_key=True)  # 商品编号 主键
    want = Column(FLOAT, nullable=False)  # 期望价格
    status = Column(BOOLEAN, nullable=False)  # 运行状态
    history = relationship('History', back_populates='goods', lazy='dynamic', cascade='all, delete-orphan')  # 一对多


# 定义映射类History(Child)
class History(Base):
    __tablename__ = 'history'
    date = Column(Integer, primary_key=True)  # 历史日期 主键
    price = Column(FLOAT, nullable=False)  # 历史价格
    gid = Column(String(20), ForeignKey('goods.id', ondelete='CASCADE'), primary_key=True)  # 外键+主键
    goods = relationship('Goods', back_populates="history")  # 一对多


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
            item['id'] = goods.id
            item['want'] = goods.want
            item['status'] = goods.status
            item['history_date'] = []
            item['history_price'] = []
            for history in goods.history:
                item['history_date'].append(history.date)
                item['history_price'].append(history.price)
            result[goods.id] = item
        return result

    def add(self, id, want, status):
        goods = Goods(id=id, want=want, status=status)
        self.session.add(goods)
        self.session.commit()

    # Goods -> History -> date price
    def add_history(self, id, date, price):
        goods = self.session.query(Goods).filter_by(id=id).first()
        goods.history.append(History(date=date, price=price))
        self.session.add(goods)
        self.session.commit()

    # Goods -> History -> date price
    def update_history(self, gid, date, price):
        history = self.session.query(History).filter_by(gid=gid, date=date).first()
        history.price = price
        self.session.commit()

    def update_want(self, id, want):
        goods = self.session.query(Goods).filter_by(id=id).first()
        goods.want = want
        self.session.commit()

    def update_status(self, id, status):
        goods = self.session.query(Goods).filter_by(id=id).first()
        goods.status = status
        self.session.commit()

    def delete(self, id):
        goods = self.session.query(Goods).filter_by(id=id).first()
        self.session.delete(goods)
        self.session.commit()


if __name__ == '__main__':
    db = DB()

    print("添加测试：")
    db.add('111111', 111.00, False)
    db.add_history('111111', 1574179200, 123.00)
    db.add_history('111111', 1574265600, 123.00)
    print(db.query())

    print("修改测试：")
    db.update_want('111111', 111.11)
    db.update_status('111111', True)
    db.update_history('111111', 1574265600, 122.00)
    print(db.query())

    print("删除测试：")
    db.delete('111111')
    print(db.query())

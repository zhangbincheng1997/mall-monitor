# import os
# import sys
#
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import logging
# from logging.handlers import TimedRotatingFileHandler

# def init_log(log_file='log/info.log'):
#     """
#     按天对日志进行分割
#     when: D天 / H小时 / M分钟
#     interval: 滚动周期
#     backupCount: 备份个数
#     """
#     handler = TimedRotatingFileHandler(log_file, when="D", interval=1, backupCount=7)
#     formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
#     handler.setFormatter(formatter)
#     logger = logging.getLogger()
#     logger.setLevel(logging.INFO)
#     logger.addHandler(handler)
#     return logger
#
#
# logger = init_log()

from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_url_path='')

from goods import Goods
import time
import json

goodsDict = {}
goodsDict['4311178'] = Goods('4311178', 219.00, '金士顿(Kingston) 240GB SSD固态硬盘 SATA3.0接口 A400系列', 229.00,
                             time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
goodsDict['4311182'] = Goods('4311182', 339.00, '金士顿(Kingston) 480GB SSD固态硬盘 SATA3.0接口 A400系列', 349.00,
                             time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
goodsDict['100002795959'] = Goods('100002795959', 4900.00,
                                  '华为 HUAWEI P30 Pro 超感光徕卡四摄10倍混合变焦麒麟980芯片屏内指纹 8GB+128GB极光色全网通版双4G手机',
                                  4988.00, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
goodsDict['100004751037'] = Goods('100004751037', 5600.00,
                                  '华为(HUAWEI)MateBook 14 第三方Linux版 全面屏轻薄性能笔记本电脑(i5-8265U 8+512GB 2k 独显)灰',
                                  5699.00, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
goodsDict['8797490'] = Goods('8797490', 8998.00, '微星（MSI）万图师 GeForce RTX 2080 Ti VENTUS GP 11G GDDR6 时尚精巧电脑电竞游戏小卡显卡',
                             8999.00, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

email = '15521106350'  # 电子邮箱
rate = 60  # 刷新频率


@app.route('/', methods=['GET'])
def view():
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add():
    data = request.form.to_dict()
    if data != '':
        id = data['id']
        print(id, goodsDict.keys())
        if id not in goodsDict.keys():
            want = float(data['want'])
            print(want)
            goodsDict[id] = Goods(id, want, '测试' + id, want + 10,
                                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            return 'yes'
        else:
            return 'no'


@app.route('/remove', methods=['POST'])
def remove():
    data = request.form.to_dict()
    if data != '':
        id = data['id']
        if id in goodsDict.keys():
            goodsDict.pop(id)
            return 'yes'
        else:
            return 'no'


@app.route('/change', methods=['POST'])
def change():
    data = request.form.to_dict()
    if data != '':
        id = data['id']
        status = data['status']
        if id in goodsDict.keys():
            print(status)
            goodsDict[id].change(status)
            return 'yes'
        else:
            return 'no'


@app.route('/setup', methods=['POST'])
def setup():
    data = request.form.to_dict()
    if data != '':
        _email = data['email']
        _rate = int(data['rate'])
        if _email is not None and _rate is not None:
            global email
            global rate
            email = _email
            rate = _rate
            return 'yes'
        else:
            return 'no'


@app.route('/get_setup', methods=['GET'])
def get_setup():
    return {'phone': phone, 'rate': rate}


@app.route('/get', methods=['GET'])
def get():
    result = []
    for item in goodsDict.values():
        result.append(item.__dict__)
    return json.dumps(result)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

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

from flask import Flask, render_template, request
from monitor import Monitor
import json

app = Flask(__name__, static_url_path='')
monitor = Monitor()
monitor.run()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add():
    data = request.form.to_dict()
    if data != '':
        id = data['id']
        want = float(data['want'])
        res = monitor.add(id, want)
        if res:
            return 'yes'
        else:
            return 'no'


@app.route('/remove', methods=['POST'])
def remove():
    data = request.form.to_dict()
    if data != '':
        id = data['id']
        res = monitor.remove(id)
        if res:
            return 'yes'
        else:
            return 'no'


@app.route('/change', methods=['POST'])
def change():
    data = request.form.to_dict()
    if data != '':
        id = data['id']
        status = data['status']
        if id in monitor.goodsDict.keys():
            monitor.goodsDict[id].change(status)
            return 'yes'
        else:
            return 'no'


@app.route('/setting', methods=['GET'])
def setting_get():
    return {'email': monitor.email, 'rate': monitor.rate}


@app.route('/setting', methods=['POST'])
def setting_set():
    data = request.form.to_dict()
    if data != '':
        email = data['email']
        rate = int(data['rate'])
        if email is not None and rate is not None:
            monitor.setting(email, rate)
            return 'yes'
        else:
            return 'no'


@app.route('/get', methods=['GET'])
def get():
    result = []
    for item in monitor.goodsDict.values():
        result.append(item.__dict__)
    return json.dumps(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

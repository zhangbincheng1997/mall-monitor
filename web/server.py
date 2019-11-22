from flask import Flask, render_template, request
from monitor import Monitor
from response import Response
import time

app = Flask(__name__, static_url_path='')
monitor = Monitor()
monitor.run()  # 启动监控


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add():
    data = request.form.to_dict()
    if data != '':
        id = data['id']
        want = float(data['want'])
        status = data['status'] == 'true'
        res = monitor.add(id, want, status)
        if res:
            return Response.success(message='添加成功')
        else:
            return Response.failure(message='商品已存在')


@app.route('/remove', methods=['POST'])
def remove():
    data = request.form.to_dict()
    if data != '':
        id = data['id']
        res = monitor.remove(id)
        if res:
            return Response.success(message='删除成功')
        else:
            return Response.failure(message='商品不存在')


@app.route('/want/update', methods=['POST'])
def update_want():
    data = request.form.to_dict()
    if data != '':
        id = data['id']
        want = float(data['want'])
        res = monitor.update_want(id, want)
        if res:
            return Response.success(message='修改成功')
        else:
            return Response.failure(message='商品不存在')


@app.route('/status/update', methods=['POST'])
def update_status():
    data = request.form.to_dict()
    if data != '':
        id = data['id']
        status = data['status'] == 'true'
        res = monitor.update_status(id, status)
        if res:
            return Response.success(message='修改成功')
        else:
            return Response.failure(message='商品不存在')


@app.route('/setting', methods=['GET'])
def setting_get():
    return Response.success(data={'email': monitor.email, 'rate': monitor.rate})


@app.route('/setting', methods=['POST'])
def setting_set():
    data = request.form.to_dict()
    if data != '':
        email = data['email']
        rate = int(data['rate'])
        if email and rate:
            monitor.email = email
            monitor.rate = rate
            return Response.success(message='设置成功')
        else:
            return Response.failure(message='请输入电子邮箱和刷新频率')


@app.route('/get', methods=['GET'])
def get():
    result = []
    for item in monitor.goods_dict.values():
        goods = {}
        goods['id'] = item.id  # 商品编号
        goods['want'] = item.want  # 期望价格
        goods['name'] = item.name  # 商品名称
        goods['price'] = item.price  # 当前价格
        goods['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item.date))  # 记录日期
        goods['status'] = item.status  # 运行状况
        result.append(goods)
    return Response.success(data=result)


@app.route('/history', methods=['GET'])
def history():
    data = request.args.to_dict()
    if data != '':
        id = data['id']
        if id in monitor.goods_dict.keys():
            history = {}
            history['price'] = monitor.goods_dict[id].history_price  # 历史价格
            history['date'] = [time.strftime('%Y-%m-%d %H:00:00', time.localtime(date))
                               for date in monitor.goods_dict[id].history_date]  # 历史日期
            return Response.success(data=history)
        else:
            return Response.failure(message='商品编号错误')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)  # 防止debug=True状态初始化两次

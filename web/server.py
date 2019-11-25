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


@app.route('/email/add', methods=['POST'])
def add_email():
    data = request.form.to_dict()
    if data != '':
        email = data['email']
        if email not in monitor.email:
            monitor.email.append(email)
            return Response.success(message='添加成功')
        else:
            return Response.failure(message='邮箱已存在')


@app.route('/email/remove', methods=['POST'])
def remove_email():
    data = request.form.to_dict()
    if data != '':
        email = data['email']
        if email in monitor.email:
            monitor.email.remove(email)
            return Response.success(message='删除成功')
        else:
            return Response.failure(message='邮箱不存在')


@app.route('/setting/update', methods=['POST'])
def update_setting():
    data = request.form.to_dict()
    if data != '':
        rate = int(data['rate'])
        note = int(data['note'])
        if rate and note:
            monitor.rate = rate
            monitor.note = note
            return Response.success(message='设置成功')
        else:
            return Response.failure(message='请输入刷新频率和通知频率')


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


@app.route('/get', methods=['GET'])
def get():
    result = []
    for item in monitor.goods_dict.values():
        goods = {}
        goods['id'] = item.id  # 商品编号
        goods['want'] = item.want  # 期望价格
        goods['status'] = item.status  # 运行状况
        goods['url'] = item.url  # 购买链接
        goods['name'] = item.name  # 商品名称
        goods['price'] = item.price  # 当前价格
        goods['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item.date))  # 记录日期
        result.append(goods)
    data = {'goods': result, 'rate': monitor.rate, 'note': monitor.note, 'email': monitor.email}
    return Response.success(data=data)


@app.route('/history', methods=['GET'])
def history():
    data = request.args.to_dict()
    if data != '':
        id = data['id']
        res = monitor.history(id)
        if history:
            return Response.success(data=res)
        else:
            return Response.failure(message='商品编号错误')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)  # 防止debug=True状态初始化两次

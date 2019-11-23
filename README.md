# mall-monitor
电商平台价格监控

![alt text](image.png)

## 技术
1. 前端：Boostrap+Jquery
2. 后端：Python+Flask
3. 爬虫：requests+beautifulsoup4+PyExecJS(未来可以加代理池)

## 启动
```
python server.py
```

## 爬虫
1. 爬取名字
https://item.jd.com/4311178.html
```
soup = BeautifulSoup(response.text, 'html.parser')
name = soup.find(class_='sku-name')
```

2. 爬取价格
https://p.3.cn/prices/mgets?skuIds=4311178
```
[
  {
    "cbf": "0",
    "id": "J_4311178",
    "m": "800.00",
    "op": "399.00",
    "p": "219.00"
  }
]
```

3. 爬取历史价格
http://tool.manmanbuy.com/history.aspx?DA=1&action=gethistory&url=http://item.jd.com/4311178.html&bjid=&spbh=&cxid=&zkid=&w=951&token=hbo5aec0bfd10dad3242ed1e5614d57c9b2f349auz8t
(根据ID从`MMM_GET_TOKEN.js`获取token)
```
{
  "datePrice": "[1508774400000,629.00,\"\"],......"
  ......
}
```

## 数据库
Goods:

| 属性 | 解释 | 类型 | 备注 |
| :----: | :----: | :----: | :----: |
| id | 商品编号 | String(20) | primary_key=True |
| want | 期望价格 | FLOAT | nullable=False |
| status | 运行状态 | BOOLEAN | nullable=False |

## 邮箱
修改`config.cfg`的参数，可以上网搜索怎么申请qq邮箱smtp密码~
```
[mail]
host     = smtp.qq.com
port     = 25
user     = xxxxxxxxxx@qq.com
pass     = xxxxxxxxxxxxxxxx
sender   = xxxxxxxxxx@qq.com
```
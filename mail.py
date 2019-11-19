import smtplib
from email.mime.text import MIMEText
from email.header import Header

mail_host = 'smtp.qq.com'
mail_port = 25
mail_user = '1656704949@qq.com'
mail_pass = 'cbsalgsbgpmabdhh'

sender = '1656704949@qq.com'
receivers = ['1656704949@qq.com', '2575941820@qq.com']

_text = '商品名称：%s\n目前价格：%.2f\n购买链接：%s' % \
        ('金士顿(Kingston) 240GB SSD固态硬盘 SATA3.0接口 A400系列', 219.00, 'https://item.jd.com/4311178.html')
_subject = '降价通知'
_from = '东哥'
_to = '东哥的兄弟'
message = MIMEText(_text, 'plain', 'utf-8')
message['Subject'] = Header(_subject, 'utf-8')
message['From'] = Header(_from, 'utf-8')
message['To'] = Header(_to, 'utf-8')

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, mail_port)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print('发送成功')
except smtplib.SMTPException:
    print('发送失败')

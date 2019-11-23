import smtplib
from email.mime.text import MIMEText
from email.header import Header
import configparser


class Mail:
    def __init__(self, config='config.cfg'):
        cfg = configparser.ConfigParser()
        cfg.read(config)
        self.mail_host = cfg.get('mail', 'host')
        self.mail_port = cfg.get('mail', 'port')
        self.mail_user = cfg.get('mail', 'user')
        self.mail_pass = cfg.get('mail', 'pass')
        self.sender = cfg.get('mail', 'sender')

    def send(self, email, name, price, want, high, low, url):
        text = '商品名称：%s\n目前价格：%.2f\n期望价格：%.2f\n历史最高：%.2f\n历史最低：%.2f\n购买链接：%s' % \
               (name, price, want, high, low, url)
        message = MIMEText(text, 'plain', 'utf-8')
        message['Subject'] = Header('降价通知', 'utf-8')
        message['From'] = Header('东哥', 'utf-8')
        message['To'] = Header('东哥的兄弟', 'utf-8')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, self.mail_port)
            smtpObj.login(self.mail_user, self.mail_pass)
            smtpObj.sendmail(self.sender, email, message.as_string())
            print('发送成功')
        except smtplib.SMTPException:
            print('发送失败')


if __name__ == '__main__':
    mail = Mail()
    mail.send('1656704949@qq.com', '金士顿(Kingston) 240GB SSD固态硬盘 SATA3.0接口 A400系列',
              219.00, 219.00, 400.00, 200.00, 'https://item.jd.com/4311178.html')

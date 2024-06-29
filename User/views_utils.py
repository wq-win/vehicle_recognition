import hashlib
import random

from django.core.mail import send_mail
from django.template import loader

from djangoGraduationProject.settings import EMAIL_HOST_USER, SERVER_HOST, SERVER_PORT


# 验证码模块，返回随机颜色
def get_color():
    return random.randrange(256)


# 验证码模块，返回随机4个字符
def generate_code():
    source = "zxcvbnmasdfghjklqwertyuiop1234567890"

    code = ""

    for i in range(4):
        code += random.choice(source)

    return code


def hash_str(source):
    return hashlib.new('sha512', source.encode('utf-8')).hexdigest()


# 发送激活用户邮件
def send_email_activate(username, receive, u_token):
    # 主题
    subject = '%s vms Activate' % username

    from_email = EMAIL_HOST_USER

    # recipient_list = ['1498760618@qq.com' ]
    recipient_list = [receive, ]

    data = {
        'username': username,
        'activate_url': 'http://{}:{}/user/activate/?u_token={}'.format(SERVER_HOST, SERVER_PORT, u_token),
    }

    html_message = loader.get_template('user/activate.html').render(data)

    send_mail(subject, message="", html_message=html_message, from_email=from_email, recipient_list=recipient_list)
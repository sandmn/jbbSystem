# -*- coding:utf-8 -*-
__author__ = 'yanxuechun'
__date__ = '2019/4/11 15:31'

from users.models import EmailVerifyRecord
from JBBSystem.settings import EMAIL_FROM
from random import Random
from django.core.mail import send_mail
def random_str(randomlength = 8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random(0,length)]
    return str


# 注册和找回密码邮箱激活
def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_time = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "金宝贝在线注册激活链接"
        email_body = "请点击连接激活：http://127.0.0.1:8000/active/{0}".format()

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "金宝贝在线注册密码重置连接"
        email_body = "请点击链接重置密码：http://127.0.0.1:8000/reset/{0}".format()
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "update_email":
        email_title = "金宝贝在线邮箱修改验证码"
        email_body = "你的邮箱验证码为：{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass


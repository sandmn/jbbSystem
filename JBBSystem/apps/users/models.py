# _*_ encoding:utf-8 _*_
# python自带的库
from __future__ import unicode_literals
from datetime import datetime


# 第三方库
from django.db import models
# 继承django自带的user表
from django.contrib.auth.models import AbstractUser

# 自己定义的model

# Create your models here.


# 在继承的基础上，自己再添加一些字段
# 自定义UserProfile覆盖默认的User表
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default="")
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(choices=(("male", u"男"), ("female", u"女")), max_length=10, default="female")  # 性别
    address = models.CharField(max_length=100, default=u"")
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    def get_unread_nums(self):
        # 获取用户未读消息的数量
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


# 邮箱验证码
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(verbose_name=u"验证码类型", choices=(("register", u"注册"),
                                                                 ("forget", u"找回密码"), ("update_email", u"修改邮箱")), max_length=30)  # 在注册和找回密码时都需要验证码
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


# 轮播图
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)  # 存储的是路径
    url = models.URLField(max_length=200, verbose_name=u"访问地址")  # 点击图片之后的跳转
    index = models.IntegerField(default=100, verbose_name=u"顺序")  # 图片的顺序
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")  # 表的生成时间

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

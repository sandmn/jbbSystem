# _*_ encoding:utf-8 _*_
from datetime import datetime
from DjangoUeditor.models import UEditorField
from django.db import models

from users.models import UserProfile
from courses.models import Course

# Create your models here.


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"姓名")
    mobile = models.CharField(max_length=11, verbose_name=u"手机")
    course_name = models.CharField(max_length=50, verbose_name=u"课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户咨询"
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    "课程评论"
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    course = models.ForeignKey(Course, verbose_name=u"课程")
    comments = models.CharField(max_length=200, verbose_name=u"评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程评论"
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    fav_id = models.IntegerField(default=0, verbose_name=u"数据id")
    fav_type = models.IntegerField(choices=((1, "课程"), (2, "课程机构"), (3, "讲师")), default=1, verbose_name=u"收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name


class UserApply(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    fav_id = models.IntegerField(default=0, verbose_name=u"数据id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u'用户报名'
        verbose_name_plural = verbose_name


class UserAppointment(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    fav_id = models.IntegerField(default=0, verbose_name=u"数据id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u'用户预约'
        verbose_name_plural = verbose_name


class UserEstimate(models.Model):
    """
    用户满意度评估
    """
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    estimate = models.IntegerField(default=0, verbose_name=u"满意度")  # 1,2,3，4 优良中差
    # estimate = models.CharField(choices=(("best", u"优"), ("good", u"良"), ("normal", u"中"),
    # ("bad", u"差")), max_length=10, default="best")  # 性别
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u"接受用户") # 0 发给全部人员，
    message = models.CharField(max_length=500, verbose_name=u"消息内容")
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    course = models.ForeignKey(Course, verbose_name=u"课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"学习时间")

    class Meta:
        verbose_name = u"用户课程"
        verbose_name_plural = verbose_name


class UserTimeTable(models.Model):
    user = models.IntegerField(default=0, verbose_name=u"接受用户")  # 0 发给全部人员，
    # timetable = UEditorField(verbose_name=u"课表", width=600, height=300, toolbars="full",
    # imagePath="operation/ueditor", filePath="operation/ueditor", default="")

    timetable = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", verbose_name=u"课表", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"学习时间")


    class Meta:
        verbose_name = u"用户课表"
        verbose_name_plural = verbose_name

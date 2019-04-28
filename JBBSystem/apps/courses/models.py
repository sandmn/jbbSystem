# _*_ encoding:utf-8 _*_
from datetime import datetime
from DjangoUeditor.models import UEditorField

from django.db import models
from organization.models import CourseOrg, Teacher

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名称")
    # type = models.CharField(verbose_name=u"课程类型", default="", choices=(("cg", "常规课"), ("zt", "主题课")), max_length=3)
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    teacher = models.ForeignKey(Teacher, verbose_name=u"讲师", null=True, blank=True)
    # detail = models.CharField(max_length=300, verbose_name=u"课程详情")

    detail = UEditorField(verbose_name=u"课程详情", width=600, height=300, toolbars="full",imagePath="courses/ueditor", filePath="courses/ueditor", default="")
    is_detail = models.BooleanField(default=True, verbose_name=u"是否详细课程")
    degree = models.CharField(verbose_name=u"难度", choices=(("cj", "初级"), ("zj", "中级"), ("gj", ("高级"))), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u"课时数")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    limit = models.IntegerField(default=0, verbose_name=u"人数上限")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.IntegerField(default=0,  verbose_name=u"课程类别")  # 0表示常规课，1表示主题课
    tag = models.CharField(default="", verbose_name=u"课程标签", max_length=10)
    time = models.CharField(default="", max_length=300, verbose_name=u"活动时间")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name=u"老师告诉你")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()
    # 后台管理系统中该字段的名称
    get_zj_nums.short_description = "章节数"

    def go_to(self):
        # 直接将文本显示
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.baidu.com'>跳转</>")
    go_to.short_description = "跳转"

    def get_learn_users(self):
        """
        获取学习用户
        usercourse相当于类UserCourse的一个实例，该类中包含字段：课程和用户
        所以要获取用户，可以先获取该类的实例，再获取用户
        :return:
        """
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        """
        获取课程所有章节,类Lesson包含字段：外键课程，章节名，学习时长
        :return:
        """
        return self.lesson_set.all()

    def __str__(self):
        return self.name  # self表示当前实例


# 同一个课程model注册两个管理器CourseAdmin，BannerCourseAdmin
class BannerCourse(Course):
    class Meta:
        verbose_name = u"轮播课程"
        verbose_name_plural = verbose_name
        # 该参数为true时，不会再生成一张表，而是和Course公用一张表
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")  # 有改变
    name = models.CharField(max_length=100, verbose_name=u"章节名称")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_video(self):
        # 获取章节视频，Lesson是video的外键
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节") # 有改变
    name = models.CharField(max_length=100, verbose_name=u"视频名称")
    url = models.CharField(max_length=200, default="", verbose_name=u"访问地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResourse(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="courses/resourse/%Y/%m", verbose_name=u"资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# -*- coding:utf-8 -*-
__author__ = 'yanxuechun'
__date__ = '2019/4/10 11:21'

import xadmin
from .models import Course, Video, Lesson, CourseResourse, BannerCourse
from organization.models import CourseOrg


# 添加课程的同时添加章节
class LessonInline(object):
    model = Lesson
    extra = 0


# 添加课程的同时可以添加课程资源
class CourseResourseInline(object):
    model = CourseResourse
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students',
                    'fav_nums', 'image', 'click_nums', 'get_zj_nums', 'go_to', 'add_time']  # 设置记录显示的字段
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students',
                     'fav_nums', 'image', 'click_nums']  # 设置搜索的字段
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students',
                   'fav_nums', 'image', 'click_nums', 'add_time']  # 设置过滤器
    # 根据点击数进行排序显示
    ordering = ['-click_nums']

    # 设置只读字段
    readonly_fields = ['click_nums']
    # 设置直接在后台界面编辑的字段
    list_editable = ['degree', 'desc']
    # 设置不显示的字段，该字段与只读字段相矛盾
    # exclude = ['fav_nums']
    # 添加课程的同时添加章节和课程资源
    inlines = [LessonInline, CourseResourseInline]
    # 设置页面刷新的时间间隔
    # refresh_times = [3, 5]
    # 设置课程详情可以通过ueditor进行文本编辑
    style_fields = {"detail": "ueditor"}
    # 添加课程时可以导入excel文件
    import_excel = True

    # def queryset(self):
    #     """
    #     前端页面显示时对课程中的数据进行过滤,过滤不是轮播图的课程
    #     :return:
    #     """
    #     qs = super(CourseAdmin, self).queryset()
    #     qs = qs.filter(is_banner=False)
    #     return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    # def post(self, request, *args, **kwargs):
    #     if 'excel' in request.FILES:
    #         pass
    #     return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students',
                    'fav_nums', 'image', 'click_nums', 'add_time']  # 设置记录显示的字段
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students',
                     'fav_nums', 'image', 'click_nums']  # 设置搜索的字段
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students',
                   'fav_nums', 'image', 'click_nums', 'add_time']  # 设置过滤器
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']
    # 添加课程的同时添加章节很课程资源
    inlines = [LessonInline, CourseResourseInline]

    def queryset(self):
        """
            前端页面显示时对课程中的数据进行过滤,过滤是轮播图的课程
            :return:
        """
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']  # 设置记录显示的字段
    search_fields = ['course', 'name']  # 设置搜索的字段
    list_filter = ['course__name', 'name', 'add_time']  # 设置过滤器，注意外键书写：course__name


class VedioAdmin(object):
    list_display = ['lesson', 'name', 'add_time']  # 设置记录显示的字段
    search_fields = ['lesson', 'name']  # 设置搜索的字段
    list_filter = ['lesson__name', 'name', 'add_time']  # 设置过滤器，注意外键书写：course__name
    # 图标显示
    model_icon = 'fa fa-film'


class CourseResourseAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']  # 设置记录显示的字段
    search_fields = ['course', 'name', 'download']  # 设置搜索的字段
    list_filter = ['course__name', 'name', 'download', 'add_time']  # 设置过滤器，注意外键书写：course__name


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VedioAdmin)
xadmin.site.register(CourseResourse, CourseResourseAdmin)

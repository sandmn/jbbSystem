# -*- coding:utf-8 -*-
__author__ = 'yanxuechun'
__date__ = '2019/4/10 14:04'

import xadmin

from .models import UserAsk, CourseComments, UserFavorite, UserApply, UserMessage, UserCourse


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']  # 设置记录显示的字段
    search_fields = ['name', 'mobile', 'course_name']  # 设置搜索的字段
    list_filter = ['name', 'mobile', 'course_name', 'add_time']  # 设置过滤器，注意外键书写：course__name
    model_icon = 'fa fa-question-circle'


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']  # 设置记录显示的字段
    search_fields = ['user', 'course', 'comments']  # 设置搜索的字段
    list_filter = ['user', 'course', 'comments', 'add_time']  # 设置过滤器，注意外键书写：course__name
    model_icon = 'fa fa-question-circle'


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']  # 设置记录显示的字段
    search_fields = ['user', 'fav_id', 'fav_type']  # 设置搜索的字段
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']  # 设置过滤器，注意外键书写：course__name
    model_icon = 'fa fa-question-circle'


class UserApplyAdmin(object):
    list_display = ['user', 'fav_id', 'add_time']  # 设置记录显示的字段
    search_fields = ['user', 'fav_id']  # 设置搜索的字段
    list_filter = ['user', 'fav_id',  'add_time']  # 设置过滤器，注意外键书写：course__name
    model_icon = 'fa fa-question-circle'


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']  # 设置记录显示的字段
    search_fields = ['user', 'message', 'has_read']  # 设置搜索的字段
    list_filter = ['user', 'message', 'has_read', 'add_time']  # 设置过滤器，注意外键书写：course__name
    model_icon = 'fa fa-question-circle'


class UserCourseAdmin(object):

    list_display = ['user', 'course', 'add_time']  # 设置记录显示的字段
    search_fields = ['user', 'course']  # 设置搜索的字段
    list_filter = ['user', 'course', 'add_time']  # 设置过滤器，注意外键书写：course__name
    model_icon = 'fa fa-question-circle'


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserApply, UserApplyAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)

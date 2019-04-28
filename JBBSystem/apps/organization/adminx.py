# -*- coding:utf-8 -*-
__author__ = 'yanxuechun'
__date__ = '2019/4/10 14:20'

import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']  # 设置记录显示的字段
    search_fields = ['name', 'desc']  # 设置搜索的字段
    list_filter = ['name', 'desc', 'add_time']  # 设置过滤器，注意外键书写：course__name
    model_icon = 'fa fa-university'


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_num', 'fav_num', 'image', 'address', 'city',  'add_time']  # 设置记录显示的字段
    search_fields = ['name', 'desc', 'click_num', 'fav_num', 'image', 'address', 'city']  # 设置搜索的字段
    list_filter = ['name', 'desc', 'click_num', 'fav_num', 'image', 'address', 'city__name',  'add_time']  # 设置过滤器，注意外键书写：course__name
    # 对课程机构字段进行搜索，而不是下拉所有字段
    # relfield_style = 'fk-ajax'
    model_icon = 'fa fa-university'
    style_fields = {"desc": "ueditor"}


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_num', 'add_time']  # 设置记录显示的字段
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_num']  # 设置搜索的字段
    list_filter = ['org__name', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_num', 'add_time']  # 设置过滤器，注意外键书写：course__name
    style_fields = {"points": "ueditor"}
    model_icon = 'fa fa-university'


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)

# -*- coding:utf-8 -*-
__author__ = 'yanxuechun'
__date__ = '2019/4/14 17:30'

from django.conf.urls import url, include
from .views import CourseListView, MyCourseListView,  CourseDetailView, MyCourseDetailView,  CourseInfoView, CommentsView, AddCommentsView

urlpatterns = [
    # 详细课程首页
    url(r'^list/$', CourseListView.as_view(), name="course_list"),

    # 概括课程首页
    url(r'^mylist/$', MyCourseListView.as_view(), name="mycourse_list"),

    # 详细课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),

    # 概括课程详情页
    url(r'^mydetail/(?P<course_id>\d+)/$', MyCourseDetailView.as_view(), name="mycourse_detail"),

    # 课程章节
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),

    # 课程评论
    url(r'^comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name="course_comment"),

    # 添加课程评论
    url(r'^add_comment/$', AddCommentsView.as_view(), name="add_comment"),

]
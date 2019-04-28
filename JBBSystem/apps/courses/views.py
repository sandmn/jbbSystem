# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite, UserApply, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


from .models import Course, CourseResourse
from users.models import Banner
# Create your views here.


class CourseListView(View):
    def get(self, request):
        # 根据添加时间获取所有课程
        all_courses = Course.objects.filter(is_detail=True).order_by('-add_time')

        # 根据点击数获取热门课程
        hot_courses = Course.objects.filter(is_detail=True).order_by('-click_nums')

        # 课程搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q (detail__icontains=search_keywords))

        # 课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "cg":
                all_courses = all_courses.filter(category=0)
                # all_courses = all_courses.order_by("-students")
            elif sort == "zt":
                all_courses = all_courses.filter(category=1)
                # all_courses = all_courses.order_by("-click_nums")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)     # 5表示每一页的数量

        all_courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': all_courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


class MyCourseListView(View):
    """
    课程介绍页  这里的is_banner变量代表的是 日常课程（具体课程）还是课程介绍中的课程（概括课程）
    is_banner:True表示概括课程，False表示日常课程
    这里取出的是概括课程
    """
    def get(self, request):
        # # 取出轮播图
        # all_banners = Banner.objects.all().order_by('index')

        # 取出概括课程
        all_courses = Course.objects.filter(is_detail=False)

        # 课程搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                    detail__icontains=search_keywords))

        # 课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "cg":
                all_courses = all_courses.filter(category=0)
                # all_courses = all_courses.order_by("-students")
            elif sort == "zt":
                all_courses = all_courses.filter(category=1)
                # all_courses = all_courses.order_by("-click_nums")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)  # 5表示每一页的数量

        all_courses = p.page(page)

        # banner_courses = Course.objects.filter(is_banner=True)
        return render(request, 'mycourse-list.html', {
            # 'all_banners': all_banners,
            'all_courses': all_courses,
            # 'banner_courses': banner_courses,
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击报名数
        course.click_nums += 1
        course.save()

        # 是否收藏课程
        has_fav_course = False
        # 是否收藏机构
        has_fav_org = False
        # 是否报名
        has_apply_name = False

        # 如果用户登陆
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
            if UserApply.objects.filter(user=request.user, fav_id=course.id):
                has_apply_name = True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request, "course-detail.html", {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
            'has_apply_name': has_apply_name
        })


class MyCourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        return render(request, "mycourse-detail.html", {
            'course': course,
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        course.students += 1
        course.save()
        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_cousers = UserCourse.objects.filter(course=course)
        user_ids = [user_couser.user.id for user_couser in user_cousers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        # 获取该用户学过的其他所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resources = CourseResourse.objects.filter(course=course)
        return render(request, "course-video.html", {
            'course': course,
            'course_resources': all_resources,
            'relate_courses': relate_courses
        })


class CommentsView(LoginRequiredMixin, View):
    """
    课程评论信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResourse.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course).order_by("-id")
        return render(request, "course-comment.html", {
            'course': course,
            'course_resources': all_resources,
            'all_comments': all_comments,
        })


class AddCommentsView(View):
    # 用户添加课程评论
    def post(self, request):
        if not request.user.is_authenticated():  # 判断用户是否登陆
            # 判断用户登陆状态
            return HttpResponse("{'status':'fail', 'msg':'用户未登录'}",
                                content_type='application/json')

        # 获取用户输入的课程id和对该课程的评论
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if course_id > 0 and comments:
            # 创建课程评论的实例
            course_comments = CourseComments()
            # 获取用户评论的课程id
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse("{'status':'success', 'msg':'添加成功'}",
                                content_type='application/json')
        else:
            return HttpResponse("{'status':'fail', 'msg':'添加失败'}",
                                content_type='application/json')

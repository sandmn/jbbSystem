# _*_ encoding:utf-8 _*_
import json
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, UploadImageForm, ModifyPwdForm, UserInfoForm, ForgetForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserTimeTable,  UserFavorite, UserMessage, UserApply
from organization.models import CourseOrg, Teacher
from courses.models import Course
from .models import Banner


# 以下两部分是用户登陆模块
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # “=”后的username是参数传入的，get从数据库中获取的username和email与之对比是否相等
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 配置可以使用邮箱登陆
            # 验证密码是否正确
            if user.check_password(password):
                return user
        except Exception as e:
            return None
# Create your views here.


# 邮箱激活
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, "login.html")


# 邮箱注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = True
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册金宝贝在线"
            user_message.save()

            # 邮箱注册发送邮件
            # send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class LogoutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        # 该函数将url名反解为url字符串，然后重定向到首页
        return HttpResponseRedirect(reverse("index"))


# 继承View,
# 使用django的form自动验证
class LoginView(View):
    def get(self, request):  # 该方法会自动进行判断是否是get，不需要自己判断
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)  # 实例化form
        if login_form.is_valid():  # 如果输入合法
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)  # django提供的验证用户名和密码是否注册并对应，如果没有注册或密码错误则返回None
            if user is not None:
                    login(request, user)  # django提供的登陆函数
                    return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})  # 密码出错提示
        else:
            return render(request, "login.html", {"login_form": login_form})  # 密码出错提


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form":forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form":forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email":email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    """
    修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email":email, "msg":"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email":email, "modify_form":modify_form})


class UserinfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse("{'status':'success',}", content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse("{'status':'success',}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail',}", content_type='application/json')


class UpdatePwdView(View):
    """
    个人中心修改密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse("{'status':'fail',‘msg’:‘密码不一致’}", content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse("{'status':'success',}", content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "邮箱已经存在"}', content_type='application/json')
        send_register_email(email, 'update_email')
        return HttpResponse("{'status':'success',}", content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改个人邮箱
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type = 'update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse("{'status':'success',}", content_type='application/json')
        else:
            return HttpResponse('{"email": "验证码出错"}', content_type='application/json')


# class MyCourseView(LoginRequiredMixin, View):
#     """
#     我的课程
#     """
#     def get(self, request):
#         user_courses = UserCourse.objects.filter(user=request.user)
#         return render(request, 'usercenter-mycourse.html', {
#             'user_courses': user_courses,
#         })


class MyFavOrgView(LoginRequiredMixin, View):
    """
    我收藏的课程机构
    """
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    我收藏的授课讲师
    """
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    我收藏的课程
    """
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
        })


class MyApplyCourseView(LoginRequiredMixin, View):
    """
    我报名的课程
    """
    def get(self, request):
        course_list = []
        apply_courses = UserApply.objects.filter(user=request.user)
        for apply_course in apply_courses:
            course_id = apply_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-mycourse.html', {
            'course_list': course_list,
        })


class MyTimeTableView(LoginRequiredMixin, View):
    """
    我的课表
    """
    def get(self, request):
        all_timetable = UserTimeTable.objects.filter(user=request.user.id)

        # 对消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_timetable, 5, request=request)  # 5表示每一页的数量
        timetables = p.page(page)
        return render(request, 'usercenter-timetable.html', {
            'timetables': timetables
        })


class MymessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人信息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 5, request=request)  # 5表示每一页的数量
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'messages': messages
        })


class IndexView(View):
    """
    慕学在线网首页
    """
    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.all()[:7]
        # courses = Course.objects.filter(is_banner=False)[:6]
        # banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        teachers = Teacher.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            # 'banner_courses': banner_courses,
            'course_orgs': course_orgs,
            'teachers': teachers
        })


def page_not_found(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response


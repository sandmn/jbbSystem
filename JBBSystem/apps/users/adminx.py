# -*- coding:utf-8 -*-
__author__ = 'yanxuechun'
__date__ = '2019/4/10 10:28'

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset, Main, Side, Row
# from django.utils.translation import ugettext as _
from .models import EmailVerifyRecord, Banner, UserProfile


class UserProfileAdmin(UserAdmin):
    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Personal info'),
                             Row('first_name', 'last_name'),
                             'email'
                             ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),
                             'last_login', 'date_joined'
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserAdmin, self).get_form_layout()


class BaseSetting(object):
    enable_themes = True  # 设置主题功能，默认不设置主题
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "金宝贝早教中心管理系统"  # 标题配置
    site_footer = "金宝贝早教中心"   # 下面配置
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']  # 设置记录显示的字段
    search_fields = ['code', 'email', 'send_type']  # 设置搜索的字段
    list_filter = ['code', 'email', 'send_type', 'send_time']  # 设置过滤器
    list_editable = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-address-book-o'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']  # 设置记录显示的字段
    search_fields = ['title', 'image', 'url', 'index']  # 设置搜索的字段
    list_filter = ['title', 'image', 'url', 'index', 'add_time']  # 设置过滤器


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)


# -*- coding:utf-8 -*-
__author__ = 'yanxuechun'
__date__ = '2019/4/23 10:26'

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from  django.template import loader


# excel导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    # 返回true时，才会 加载文件
    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    # 把自己的html文件加载到页面上
    def block_top_toolbar(self, context, nodes):
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', context_instance=context))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)

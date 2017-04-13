#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from django.conf.urls import url
#导入app中的views模块
from backend import views

urlpatterns = [
#当URL中包含index时，调用views文件中的index函数处理
    url(r'^$',views.index),
    url(r'^index/',views.index),
    url(r'^upload/', views.upload),
    url(r'^article_list/', views.article_list),
    url(r'^new_article/', views.new_article),
    url(r'edit/',views.edit),
    url(r'edit_article',views.edit_article),
    url(r'save_draft',views.save_draft),
    url(r'draft',views.draft),
    url(r'delete/',views.delete),
    url(r'recycle/',views.recycle),
    url(r'test/',views.test),
]
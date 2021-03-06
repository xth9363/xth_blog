# -*- coding: utf-8 -*-
# @Time    : 2018/6/1 10:37
# @Author  : Tianhao
# @Email   : xth9363@163.com
# @File    : urls.py
# @Software: PyCharm
from django.urls import path, include
from blog import views

urlpatterns = [
    path('', views.index, name="blog_index"),
    path('article/<int:aid>', views.article_details, name="article_details"),
    path('tag/<int:tid>', views.get_tag_articcles, name="get_tag_articcles"),
    path('type/<int:tid>', views.get_type_articcles, name="get_type_articcles"),
    path('group/<int:gid>', views.get_group_articcles, name="get_group_articcles"),
    path('search/', views.article_search, name="article_search"),
    path('groups/', views.group_list, name="get_groups"),
    path('post_comment/', views.post_comment, name="post_comment"),
    path('raise_error/<int:code>', views.raise_error, name="raise_error"),
    path('my_blog_list', views.my_blog_list, name="my_blog_list"),
    # path('daily_mail', views.daily_mail, name="daily_mail"),
]

# handler404 = views.page_not_found

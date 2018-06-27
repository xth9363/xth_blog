# -*- coding: utf-8 -*-
# @Time    : 2018/6/27 10:43
# @Author  : Tianhao
# @Email   : xth9363@163.com
# @File    : tasks.py
# @Software: PyCharm

# Celery tasks
# 文件名必须为tasks.py

# Create your tasks here
# from __future__ import absolute_import, unicode_literals
# # 共享的的task,即其他app也可以使用
# from celery import shared_task
# from my_blog.settings import EMAIL_HOST_USER, ADMINS
# from django.core.mail import send_mail  # 导入django发送邮件模块
# from .models import Visitor
# import datetime
#
#
# # @shared_task
# # def daily_mail():
# #     now = datetime.datetime.now()
# #     # 今日访问量:
# #     visitor = Visitor.objects.filter(visit_date__year=now.year, visit_date__month=now.month,
# #                                      visit_date__day=now.day).count()
# #
# #     content = "{}:{}:{}".format(e.args[0], result.text, result.status_code)
# #     send_mail('获取IP所在地出错', content, EMAIL_HOST_USER, [ADMINS[0][1]], fail_silently=False)
#
#
# @shared_task
# def add(x, y):
#     return x + y
#
#
# @shared_task
# def mul(x, y):
#     return x * y
#
#
# @shared_task
# def xsum(numbers):
#     return sum(numbers)

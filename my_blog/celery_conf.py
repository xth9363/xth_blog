# -*- coding: utf-8 -*-
# @Time    : 2018/6/27 10:36
# @Author  : Tianhao
# @Email   : xth9363@163.com
# @File    : celery_conf.py
# @Software: PyCharm
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_blog.settings')

app = Celery('my_blog')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# 即celery的配置都可以放到项目的settings文件中去,且以 "Celery_"开头
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# 从所有app中加载celery的task任务
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

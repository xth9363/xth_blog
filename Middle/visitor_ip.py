# -*- coding: utf-8 -*-
# @Time    : 2018/6/9 9:15
# @Author  : Tianhao
# @Email   : xth9363@163.com
# @File    : visitor_ip.py
# @Software: PyCharm
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, HttpResponseRedirect, render_to_response

from django.utils.deprecation import MiddlewareMixin
from blog.utils import get_data
from blog.models import Visitor
import json
from my_blog import settings
from my_blog.settings import ADMINS, EMAIL_HOST_USER


def add_visitor(visitor, url=None):
    if visitor:
        Visitor.objects.create(ip=visitor['ip'],
                               url=url,
                               # location="{}|{}".format(visitor['country'], visitor['province'])
                               )


class RecordIp(MiddlewareMixin):
    def process_request(self, request):
        pass

    def process_response(self, request, response):
        visitor_data = False
        # if not settings.DEBUG:
        if True:
            try:
                if 'user_ip' not in request.session:
                    visitor_data = get_data.get_visitor_ip(request)
                    print("visitor_data",visitor_data)
                    print("visitor_data_b",bool(visitor_data))
                    if visitor_data:
                        add_visitor(visitor_data)  # 添加访客数据
                        request.session['user_ip'] = visitor_data
                    # else:
                    #     return HttpResponse(status=403)
            except Exception as e:
                pass
                # from django.core.mail import send_mail  # 导入django发送邮件模块
                # content = "{}:{}".format(e.args[0], json.dumps(visitor_data))
                # send_mail('添加访客信息出错', content, EMAIL_HOST_USER, [ADMINS[0][1]], fail_silently=False)
                # return HttpResponse(status=403)
            return response
        # ip = False
        # if 'HTTP_X_FORWARDED_FOR' in request.META:
        #     ip = request.META['HTTP_X_FORWARDED_FOR']
        # elif 'REMOTE_ADDR' in request.META:
        #     ip = request.META['REMOTE_ADDR']
        # if ip:
        #     from django.core.cache import cache  # 引入缓存模块
        #     cache.set(ip, '', 60 * 60)  # 写入key为v，值为555的缓存，有效期30分钟
        #     cache.has_key(ip)  # 判断key为v是否存在
        #     lala = cache.get(ip)  # 获取key为v的缓存
        #     print(ip,lala)
        # else:
        #     print("lplp")
        #     return HttpResponse(status=403)


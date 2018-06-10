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


def add_visitor(visitor, url=None):
    if visitor:
        Visitor.objects.create(ip=visitor['ip'], url=url,
                               location="{}|{}".format(visitor['country'], visitor['province']))


class RecordIp(MiddlewareMixin):
    def process_request(self, request):
        pass

    def process_response(self, request, response):
        if not settings.DEBUG:
            try:
                if 'user_ip' not in request.session:
                    visitor_data = get_data.get_visitor_ip(request)
                    if visitor_data:
                        print(visitor_data)
                        # try:
                        add_visitor(visitor_data)  # 添加访客数据
                        request.session['user_ip'] = visitor_data
                    else:
                        print("获取IP失败")
                        # else:
                        #     visitor_data = request.session.get('user_ip')
                        #     add_visitor(visitor_data)  # 添加访客数据
            except Exception as e:
                # raise HttpResponse('Sorry,您没有访问的权限', status=403)
                print('异常')
                print(e)
        return response


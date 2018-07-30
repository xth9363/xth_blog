# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 16:23
# @Author  : Tianhao
# @Email   : xth9363@163.com
# @File    : get_data.py
# @Software: PyCharm
from blog import models
import json
import requests as rq
from django.core.paginator import Paginator
from blog.utils._asd import is_int
from my_blog.settings import ADMINS, EMAIL_HOST_USER

LIMIT = 10


def ip_safe(ip):
    # 返回顶部栏数据
    ip_s = ip.split('.')
    ip_s[0] = "***"
    return ".".join(ip_s)


def comment_order(aid):
    all_comments = models.Comment.objects.filter(article_id=aid).order_by('add_date')
    comment_list_dict = {}
    ordered_comment = []
    for each in all_comments:
        comment_list_dict[each.id] = each
        each.cc = []
        if each.parent_id:
            comment_list_dict[each.parent_id].cc.append(each)
        else:
            ordered_comment.append(each)
    return ordered_comment
    # return []


def get_visitor_ip(req):
    ip = False
    if 'HTTP_X_FORWARDED_FOR' in req.META:
        ip = req.META['HTTP_X_FORWARDED_FOR']
    elif 'REMOTE_ADDR' in req.META:
        ip = req.META['REMOTE_ADDR']

    if ip:
        result = ""
        try:
            result = rq.get(
                'http://ip.taobao.com/service/getIpInfo.php?ip=%s' % ip)
            print(result.text)
            j_data = json.loads(result.text)['data']
            return {'ip': ip,
                    'ip_save': ip_safe(ip),
                    'country': j_data['country'],
                    'province': j_data['region'],
                    'city': j_data['city'],
                    'isp': j_data['isp']
                    }
        except Exception as e:
            from django.core.mail import send_mail  # 导入django发送邮件模块
            content = "{}:{}:{}".format(e.args[0], result.text, result.status_code)
            send_mail('获取IP所在地出错', content, EMAIL_HOST_USER, [ADMINS[0][1]], fail_silently=False)
            return False
    else:
        return False


def page_limit(rq, datas):
    p = Paginator(datas, LIMIT)
    page = int(rq.GET.get('page')) if 'page' in rq.GET and is_int(rq.GET.get('page')) and 0 < int(
        rq.GET.get('page')) <= p.num_pages  else 1
    return {'page': page, 'num': p.num_pages, 'count': p.count}, p.page(page if page > 0 and page <= p.num_pages else 1)


def order_limit(rq):
    if 'o' in rq.GET:
        return rq.GET.get('o')
    else:
        return '-add_date'

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

LIMIT = 6
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
        try:
            result = rq.get(
                'http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=%s' % ip)
            # print(result.text)
            j_data = json.loads(result.text)
            ip_split = ip.split('.')
            ip_split[3] = '*'
            ip = ".".join(ip_split)
            return '[{}][{}:{}:{}]'.format(ip, j_data['country'], j_data['province'], j_data['city'])
        except Exception as e:
            print(e)
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
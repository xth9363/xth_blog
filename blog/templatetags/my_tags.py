# -*- coding: utf-8 -*-
# @Time    : 2018/6/3 9:53
# @Author  : Tianhao
# @Email   : xth9363@163.com
# @File    : my_tags.py
# @Software: PyCharm

from django import template
from blog.utils._asd import set_var_url
from blog.models import *
from django.db.models.aggregates import Count

register = template.Library()


@register.filter('range')
def range(value):
    return range(1, value + 1)


@register.filter('range0')
def range0(value):
    return range(0, value)


@register.simple_tag
def set_url_var(*args, **kwargs):
    # 组合改变url
    return set_var_url(url=kwargs['url'], var=kwargs['var'], value=kwargs['value'])

@register.simple_tag
def side_bar(*args, **kwargs):
    # 返回侧边栏数据
    side_data = {
        'new5': Article.objects.order_by('-add_date').all()[:5],
        'read5': Article.objects.order_by('-read_times').all()[:5],
        'tag12': ArticleTag.objects.annotate(num_articles=Count('articles')).filter(num_articles__gt=0).order_by(
            '-num_articles'),
        'article_group': ArticleGroup.objects.order_by('-add_date').all()[:5]
    }
    return side_data

@register.simple_tag
def top_data(*args, **kwargs):
    # 返回顶部栏数据
    return ArticleType.objects.all()

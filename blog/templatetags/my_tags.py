# -*- coding: utf-8 -*-
# @Time    : 2018/6/3 9:53
# @Author  : Tianhao
# @Email   : xth9363@163.com
# @File    : my_tags.py
# @Software: PyCharm

from django import template
from blog.utils._asd import set_var_url

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
    return set_var_url(url=kwargs['url'],var=kwargs['var'],value=kwargs['value'])

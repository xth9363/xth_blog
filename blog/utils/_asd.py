import json
import uuid
from collections import OrderedDict
from datetime import datetime

from django import forms
from django.db.models.query import QuerySet
from django.forms import ModelForm
from django.forms import widgets
from django.forms.models import model_to_dict
import re


def dir_and_files(path):
    import os
    try:
        for root, dirs, files in os.walk(path):
            print("\033[1;31m-" * 8, "directory", "<%s>\033[0m" % root, "-" * 10)
            for directory in dirs:
                print("\033[1;34m<DIR>    %s\033[0m" % directory)
            for file in files:
                print("\t\t%s" % file)
    except OSError as ex:
        print(ex)


def get_dir(var):
    '''
    返回某个对象可以调用的所有属性名和对应的属性值
    :param var:
    :return:
    '''
    for i in dir(var):
        print(i, '=', getattr(var, i))


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        pass
    return False


def validate_title(self, title):
    '''
    :param self:
    :param title: 准备替换的文件名
    :return:返回规范的文件名
    '''
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


def mk_dir(self, path):
    '''
    判断路径文件夹是否存在,如果不存在就创建,不存在返回True,存在返回False
    :param self:
    :param path:
    :return:
    '''
    # 引入模块
    import os
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print(path + ' 目录已存在')
        return False


def get_url_var_dic(url, var=None):
    '''
    根据url,返回url中所有的参数和值的字典
    :param url:
    :return:不指定返回参数时候，返回所有参数的值和字典,如果指定了返回参数.就只返回指定参数

    '''
    u = url
    u_s = u.split("?")
    result_dic = {}
    if len(u_s) > 1:
        u_vs = u_s[1].split("&")
        for each in u_vs:
            vs = each.split("=")
            result_dic[vs[0]] = vs[1]
    # 如果指定了返回参数
    if var:
        return result_dic[var]
    else:
        return result_dic


# 设置url中的某个参数，并且返回替换后的url
def set_var_url(url, var, value):
    '''
    设置url中的某个参数，并且返回替换后的url
    :param url:
    :param var:参数名
    :param value:参数值
    :return:返回替换后的url
    '''
    import re
    host_var = url.split("?")
    result = host_var[0]
    vars = get_url_var_dic(url)
    vars[var] = str(value)
    for each, value in vars.items():
        result += "&" + each + "=" + value
    result = re.sub(r'&', "?", result, 1)
    return result


def QuerySet_to_arry(qs):
    result = []
    for each in qs:
        result.append(model_to_dict(each))
    return result


class DataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.__str__()
        if isinstance(obj, uuid.UUID):
            return obj.__str__()
            # return "123123"
        return json.JSONEncoder.default(self, obj)


def my_dumps(obj):
    # list
    if isinstance(obj, QuerySet):
        obj = QuerySet_to_arry(obj)
    return json.dumps(obj, cls=DataEncoder)

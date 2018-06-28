from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, HttpResponseRedirect, render_to_response
from django.urls import reverse

from blog import models
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count
from django.db import connection
from django.db.models import Q
import requests as rq
import json
from django.forms import forms, ModelForm, widgets
from ckeditor.fields import RichTextField
from blog.utils._asd import is_int
from django.views.decorators.cache import cache_page
from blog.utils import get_data
from my_blog.settings import ADMINS, EMAIL_HOST_USER


# Create your views here.
# @cache_page(60)
# 首页
def index(request):
    # from django.core.mail import send_mail  # 导入django发送邮件模块
    # send_mail('subject', 'message', 'xth4065@163.com', ['xth9363@163.com'], fail_silently=False)
    # raise Http404('not')
    articles = models.Article.objects.exclude(type_id=3).order_by('-add_date')[:10]
    # print(articles.query.__str__())
    context = {
        'articles': articles,
    }
    # print(context)

    return render(request, 'blog/index.html', context)


# 文章详情
def article_details(request, aid):
    article = get_object_or_404(models.Article, id=aid)
    article.read_times += 1
    article.save()
    pre_article = models.Article.objects.filter(id__lt=aid).order_by("-id").values('id', 'title').first()
    next_article = models.Article.objects.filter(id__gt=aid).values('id', 'title').first()
    # 相关
    reakated_article = models.Article.objects.filter(
        Q(group=article.group) | Q(type=article.type) | Q(tags__in=article.tags.all())).exclude(
        type_id=3).distinct().order_by('?')[
                       :10].values('id',
                                   'title')

    visitor_data = request.session['user_ip'] if 'user_ip' in request.session else False
    print(visitor_data)
    context = {
        'article': article,
        'pre_article': pre_article,
        'next_article': next_article,
        'reakated_article': reakated_article,  # 相关文章
        'comments': get_data.comment_order(aid),
        'visitor_data': visitor_data
    }
    red = render(request, 'blog/info.html', context)
    #
    # if user_ip:
    #     red.set_cookie('user_ip', json.dumps(user_ip))  # 'NoneType' object has no attribute 'split' 不能直接用中文
    #     context['user_ip'] = user_ip
    return red


# 提交评论
def post_comment(request):
    if request.method == 'POST':
        print(request.POST)
        if 'user_ip' in request.session:
            user_ip = request.session['user_ip']
            commenter = "{}|{}{}{}".format(user_ip['ip_save'],
                                           user_ip['country'],
                                           user_ip['province'],
                                           user_ip['city'])
            # commenter = "{}".format(user_ip['ip_save'])
            aid = int(request.POST.get('aid'))
            if 'parent_id' in request.POST and request.POST.get('parent_id'):
                models.Comment.objects.create(commenter=commenter,
                                              article_id=aid,
                                              content=format(request.POST.get('content')),
                                              parent_id=int(request.POST.get('parent_id')),
                                              reply_to=request.POST.get('commenter'))
            else:
                models.Comment.objects.create(commenter=commenter,
                                              article_id=int(request.POST.get('aid')),
                                              content=request.POST.get('content'), )
            article = get_object_or_404(models.Article, id=aid)
            # content = "{}|{}:{}".format(article.title, commenter, request.POST.get('content'))
            # from django.core.mail import send_mail  # 导入django发送邮件模块
            # send_mail('新的评论', content, EMAIL_HOST_USER, [ADMINS[0][1]], fail_silently=False)
            return redirect(reverse('article_details', args=[int(request.POST.get('aid')), ]))
        else:
            return HttpResponse(status=403)
    else:
        raise Http404()


# 根据tag获取文章
def get_tag_articcles(request, tid):
    tag = get_object_or_404(models.ArticleTag, id=tid)
    pages, articles = get_data.page_limit(request, tag.articles.all().order_by(get_data.order_limit(request)))
    context = {
        'articles': articles,
        'tag': tag,
        'pages': pages
    }

    print(dir(request))
    print(request.get_full_path())
    return render(request, 'blog/articles_list.html', context)


# 根据文章类型获取文章
def get_type_articcles(request, tid):
    type = get_object_or_404(models.ArticleType, id=tid)
    pages, articles = get_data.page_limit(request, type.article_set.all().order_by(get_data.order_limit(request)))
    context = {
        'articles': articles,
        'type': type,
        'pages': pages

    }
    return render(request, 'blog/articles_list.html', context)


# 根据所属组获取文章
def get_group_articcles(request, gid):
    group = get_object_or_404(models.ArticleGroup, id=gid)
    pages, articles = get_data.page_limit(request, group.article_set.all().order_by(get_data.order_limit(request)))
    context = {
        'articles': articles,
        'group': group,
        'pages': pages

    }
    return render(request, 'blog/articles_list.html', context)


# 文章搜索
def article_search(request):
    print(request.get_full_path())
    print(request.path)

    if 'keyboard' in request.GET:
        key = request.GET['keyboard']
        pages, articles = get_data.page_limit(request, models.Article.objects.filter(
            Q(content__contains=key) | Q(title__contains=key)).order_by(get_data.order_limit(request)))

        context = {
            'articles': articles,
            'key': key,
            'pages': pages

        }
        return render(request, 'blog/articles_list.html', context)
    else:
        raise Http404("请带上关键字")


# 分组
def group_list(request):
    context = {
        'groups': models.ArticleGroup.objects.all()
    }
    return render(request, 'blog/articles_group_list.html', context)


# 查看月访问量
def my_blog_list(request):
    import datetime
    import calendar
    now = datetime.datetime.now()
    month = now.month
    visitors = models.Visitor.objects.filter(visit_date__year=now.year, visit_date__month=now.month)
    # 本月总访问量
    visitors_num = visitors.count()
    # 返回本月的
    week, day_num = calendar.monthrange(now.year, now.month)
    # 这里是关键,先用extract拼接获得访问时间的具体日期中的day,然后分组,计数添加一个名为dcount的变量存储每日的访客数量
    visitors = visitors.extra(select={'day': 'extract( day from visit_date )'}).values('day').annotate(
        dcount=Count('visit_date'))
    # 排好序并填好数据的字典,先全部设为0
    visitor_dict = {i: 0 for i in range(1, day_num + 1)}
    # for i in range(1, day_num + 1):
    #     visitor_dict[i] = 0
    for each in visitors:
        visitor_dict[each['day']] = each['dcount']
    context = {
        'visitor_dict': visitor_dict,
        'visitors_num': visitors_num,
        'month': month,
    }
    return render(request, 'blog/show_visitor_data.html', context)


# 错误处理页面
def e_404(request, exception):
    return render(request, 'blog/404.html', {})


def e_500(request):  # 这里一个坑
    return render(request, 'blog/500.html', {})


def e_502(request):
    return render(request, 'blog/502.html', {})


def e_403(request):
    return render(request, 'blog/403.html', {})


def raise_error(request, code):
    from blog.utils._asd import is_int
    codes = [404, 403, 500]
    if is_int(code) and int(code) in codes:
        response = render_to_response('%s.html' % code, {})
        response.status_code = int(code)
        return response
    else:
        response = render_to_response('blog/404.html', {})
        response.status_code = 404
        return response

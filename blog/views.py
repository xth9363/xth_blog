from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, HttpResponseRedirect, render_to_response
from django.urls import reverse

from blog import models
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count
from django.db.models import Q
import requests as rq
import json
from django.forms import forms, ModelForm, widgets
from ckeditor.fields import RichTextField
from blog.utils._asd import is_int
from django.views.decorators.cache import cache_page
from blog.utils import get_data


# Create your views here.
# @cache_page(60)
def index(request):
    # from django.core.mail import send_mail  # 导入django发送邮件模块
    # send_mail('subject', 'message', 'xth4065@163.com', ['xth9363@163.com'], fail_silently=False)
    # raise Http404('not')
    articles = models.Article.objects.filter().order_by('-add_date')[:10]

    # print(articles.query.__str__())
    context = {
        'articles': articles,
    }
    # print(context)
    return render(request, 'index.html', context)


def article_details(request, aid):
    article = get_object_or_404(models.Article, id=aid)
    article.read_times += 1
    article.save()
    pre_article = models.Article.objects.filter(id__gt=aid).values('id', 'title').first()
    next_article = models.Article.objects.filter(id__lt=aid).order_by("-id").values('id', 'title').first()
    # 相关
    reakated_article = models.Article.objects.filter(
        Q(group=article.group) | Q(type=article.type) | Q(tags__in=article.tags.all())).distinct()[:10].values('id','title')

    user_ip = get_data.get_visitor_ip(request)
    context = {
        'article': article,
        'pre_article': pre_article,
        'next_article': next_article,
        'reakated_article': reakated_article,  # 相关文章
        'comments': get_data.comment_order(aid),
        'user_ip': user_ip
    }
    red = render(request, 'info.html', context)

    if user_ip:
        red.set_cookie('user_ip', json.dumps(user_ip))  # 'NoneType' object has no attribute 'split' 不能直接用中文
        context['user_ip'] = user_ip
    return red


def post_comment(request):
    if request.method == 'POST':
        print(request.POST)
        if 'user_ip' in request.COOKIES:
            if 'parent_id' in request.POST and request.POST.get('parent_id'):
                models.Comment.objects.create(commenter=json.loads(request.COOKIES.get('user_ip')),
                                              article_id=int(request.POST.get('aid')),
                                              content=format(request.POST.get('content')),
                                              parent_id=int(request.POST.get('parent_id')),
                                              reply_to=request.POST.get('commenter'))
            else:
                models.Comment.objects.create(commenter=json.loads(request.COOKIES.get('user_ip')),
                                              article_id=int(request.POST.get('aid')),
                                              content=request.POST.get('content'), )
            return redirect(reverse('article_details', args=[int(request.POST.get('aid')), ]))
        else:
            raise Http404('为了使用本功能,请开启您浏览器的Cookie')
    else:
        return Http404()


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
    return render(request, 'articles_list.html', context)


def get_type_articcles(request, tid):
    type = get_object_or_404(models.ArticleType, id=tid)
    pages, articles = get_data.page_limit(request, type.article_set.all().order_by(get_data.order_limit(request)))
    context = {
        'articles': articles,
        'type': type,
        'pages': pages

    }
    return render(request, 'articles_list.html', context)


def get_group_articcles(request, gid):
    group = get_object_or_404(models.ArticleGroup, id=gid)
    pages, articles = get_data.page_limit(request, group.article_set.all().order_by(get_data.order_limit(request)))
    context = {
        'articles': articles,
        'group': group,
        'pages': pages

    }
    return render(request, 'articles_list.html', context)


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
        return render(request, 'articles_list.html', context)
    else:
        raise Http404("请带上关键字")


def group_list(request):
    context = {
        'groups': models.ArticleGroup.objects.all()
    }
    return render(request, 'articles_group_list.html', context)


def e_404(request, exception):
    return render(request, '404.html', {})


def e_500(request):  # 这里一个坑
    return render(request, '500.html', {})


def e_502(request):
    return render(request, '502.html', {})


def e_403(request):
    return render(request, '403.html', {})


def raise_error(request, code):
    from blog.utils._asd import is_int
    codes = [404, 403, 500]
    if is_int(code) and int(code) in codes:
        response = render_to_response('%s.html' % code, {})
        response.status_code = int(code)
        return response
    else:
        response = render_to_response('404.html', {})
        response.status_code = 404
        return response

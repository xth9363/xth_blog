from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, HttpResponseRedirect, render_to_response
from django.urls import reverse

from blog import models
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count
from django.db.models import Q
import requests as rq
import json
from django.core.paginator import Paginator
from django.forms import forms, ModelForm, widgets
from ckeditor.fields import RichTextField
from blog.utils._asd import is_int

LIMIT = 6


# Create your views here.

def index(request):
    # from django.core.mail import send_mail  # 导入django发送邮件模块
    # send_mail('subject', 'message', 'xth4065@163.com', ['xth9363@163.com'], fail_silently=False)
    # raise Http404('not')
    articles = models.Article.objects.filter().order_by('-add_date')[:10]

    # print(articles.query.__str__())
    context = {
        'articles': articles,
        'side_data': sidebar_data()
    }
    # print(context)
    return render(request, 'index.html', context)


def article_details(request, aid):
    article = get_object_or_404(models.Article, id=aid)
    article.read_times += 1
    article.save()
    pre_article = models.Article.objects.filter(id__gt=aid).first()
    next_article = models.Article.objects.filter(id__lt=aid).order_by("-id").first()
    # 相关
    reakated_article = models.Article.objects.filter(
        Q(group=article.group) | Q(type=article.type) | Q(tags__in=article.tags.all())).distinct()[:10]
    comments = models.Comment.objects.filter(article_id=aid)

    user_ip = get_visitor_ip(request)
    context = {
        'article': article,
        'pre_article': pre_article,
        'next_article': next_article,
        'reakated_article': reakated_article,  # 相关文章
        'side_data': sidebar_data(),
        'comments': comment_order(aid),
        'user_ip': user_ip
    }
    red = render(request, 'info.html', context)

    if user_ip:
        red.set_cookie('user_ip', json.dumps(user_ip))  # 'NoneType' object has no attribute 'split' 不能直接用中文
        context['user_ip'] = user_ip
    return red


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
            print(result.text)
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


def page_not_found(request):
    return HttpResponse('404')


def sidebar_data():
    side_data = {
        'new5': models.Article.objects.order_by('-add_date').all()[:5],
        'read5': models.Article.objects.order_by('-read_times').all()[:5],
        'tag12': models.ArticleTag.objects.annotate(num_articles=Count('articles')).filter(num_articles__gt=0).order_by(
            '-num_articles'),
        'article_type': models.ArticleType.objects.all(),
        'article_group': models.ArticleGroup.objects.order_by('-add_date').all()[:5]
    }
    return side_data


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


def get_tag_articcles(request, tid):
    tag = get_object_or_404(models.ArticleTag, id=tid)
    pages, articles = page_limit(request, tag.articles.all().order_by(order_limit(request)))
    context = {
        'articles': articles,
        'side_data': sidebar_data(),
        'tag': tag,
        'pages': pages
    }

    print(dir(request))
    print(request.get_full_path())
    return render(request, 'articles_list.html', context)


def get_type_articcles(request, tid):
    type = get_object_or_404(models.ArticleType, id=tid)
    pages, articles = page_limit(request, type.article_set.all().order_by(order_limit(request)))
    context = {
        'articles': articles,
        'side_data': sidebar_data(),
        'type': type,
        'pages': pages

    }
    return render(request, 'articles_list.html', context)


def get_group_articcles(request, gid):
    group = get_object_or_404(models.ArticleGroup, id=gid)
    pages, articles = page_limit(request, group.article_set.all().order_by(order_limit(request)))
    context = {
        'articles': articles,
        'side_data': sidebar_data(),
        'group': group,
        'pages': pages

    }
    return render(request, 'articles_list.html', context)


def article_search(request):
    print(request.get_full_path())
    print(request.path)

    if 'keyboard' in request.GET:
        key = request.GET['keyboard']
        pages, articles = page_limit(request, models.Article.objects.filter(
            Q(content__contains=key) | Q(title__contains=key)).order_by(order_limit(request)))

        context = {
            'articles': articles,
            'side_data': sidebar_data(),
            'key': key,
            'pages': pages

        }
        return render(request, 'articles_list.html', context)
    else:
        raise Http404("请带上关键字")


def group_list(request):
    context = {
        'side_data': sidebar_data(),
        'groups': models.ArticleGroup.objects.all()
    }
    return render(request, 'articles_group_list.html', context)


def visitor(request):
    url = 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=220.175.71.177'
    return HttpResponse("查询访问用户的所属地")

import logging
def e_404(request, exception):
    logging.debug(exception)
    return render_to_response(request, '404.html', {})


def e_500(request, exception):
    logging.debug(exception)
    return render_to_response(request, '500.html', {})


def e_403(request, exception):
    logging.debug(exception)
    return render_to_response(request, '403.html', {})


# def e_404(request, exception):
#     response = render_to_response('404.html', {})
#     response.status_code = 404
#     return response
#
#
# def e_500(request, exception):
#     response = render_to_response('500.html', {})
#     response.status_code = 500
#     return response
#
#
# def e_403(request, exception):
#     response = render_to_response('403.html', {})
#     response.status_code = 403
#     return response


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

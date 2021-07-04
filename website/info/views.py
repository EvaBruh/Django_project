from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render
from .models import *


menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}]


def index(request):
    posts = Post.objects.all()
    cats = Category.objects.all()

    context = {
        'posts': posts,
        'cats': cats,
        'menu': menu,
        'title': 'Главная',
        'cat_selected': 0,
    }

    return render(request, 'info/index.html', context=context)


def about(request):
    return render(request, 'info/about.html', {'title': 'О сайте'})


def addpage(request):
    return HttpResponse('Добавить статью')


def contact(request):
    return HttpResponse('Связь')


def login(request):
    return HttpResponse('Логин')


def show_post(request, post_id):
    return HttpResponse(f'Post with post id = {post_id}')


def show_category(request, cat_id):
    posts = Post.objects.filter(cat_id=cat_id)
    cats = Category.objects.all()

    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        'cats': cats,
        'menu': menu,
        'title': 'Отображение по рубрикам',
        'cat_selected': cat_id,
    }

    return render(request, 'info/index.html', context=context)


def PageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена.</h1>')


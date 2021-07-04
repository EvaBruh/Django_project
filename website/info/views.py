from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from .models import *
# Create your views here.
menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}]


def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная',
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


def PageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена.</h1>')


from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect

from .forms import *
from .models import *


menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}]


def index(request):
    posts = Post.objects.all()

    context = {
        'posts': posts,
        'title': 'Главная',
        'cat_selected': 0,
    }

    return render(request, 'info/index.html', context=context)


def show_category(request, cat_slug):
    posts = Post.objects.filter(cat__slug=cat_slug)

    # if len(posts) == 0:
    #     raise Http404()

    context = {
        'posts': posts,
        'title': 'Отображение по рубрикам',
        'cat_selected': cat_slug,
    }

    return render(request, 'info/index.html', context=context)


def show_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)

    context = {
        'post': post,
        'title': post.title,
        'cat_selected': post.cat_id,
    }

    return render(request, 'info/post.html', context=context)


def about(request):
    return render(request, 'info/about.html', {'title': 'О сайте'})


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()

    return render(request, 'info/add_page.html', {'form': form, 'title': 'Добавить статью'})


def contact(request):
    return render(request, 'info/contact.html', {'title': 'Контакты'})


def login(request):
    return HttpResponse('Логин')


def PageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена.</h1>')


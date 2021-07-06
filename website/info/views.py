from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *


menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}]


# Домашняя страница
class PostHome(ListView):
    model = Post
    template_name = 'info/index.html'
    context_object_name = 'posts'                   # Указывает имя для переменной в index.html

    # Отображение "внутренностей", меню
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0                 # Показывает, что "Все категории" в режиме - выбрано
        return context

    # Выбрать что именно отображать, тут случай с чекером published
    def get_queryset(self):
        return Post.objects.filter(is_published=True)


# Категории
class PostCategory(ListView):
    model = Post
    template_name = 'info/index.html'
    context_object_name = 'posts'                   # Указывает имя для переменной в index.html
    allow_empty = False                             # Для вызова 404 при несуществующем URL-slug

    # Отображение "внутренностей", меню
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)    # В названии после "-" выбранная категория
        context['cat_selected'] = context['posts'][0].cat_id                # берём ID выбранной рубрики
        return context

    # Обращаемся к параметру slug из таблицы cat
    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


# Отображение поста(Читать пост)
class ShowPost(DetailView):
    model = Post
    template_name = 'info/post.html'
    slug_url_kwarg = 'post_slug'                # для id, pk_url_slug
    context_object_name = 'post'                # отображаем пост(в переменную post в post.html)

    # Функция отображения "внутренностей", меню
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = context['post']
        return context


def about(request):
    return render(request, 'info/about.html', {'title': 'О сайте'})


# "Добавить статью", отображение страницы и связь с формой
class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'info/add_page.html'

    # Функция отображения "внутренностей", меню
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Добавление статьи'
        return context


def contact(request):
    return render(request, 'info/contact.html', {'title': 'Контакты'})


def login(request):
    return HttpResponse('Логин')


def PageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена.</h1>')


from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from info.models import *
from .utils import *


# Домашняя страница
class PostHome(DataMixin, ListView):
    model = Post
    template_name = 'info/index.html'
    context_object_name = 'posts'  # Указывает имя для переменной в index.html

    # Отображение "внутренностей", меню
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return context | c_def  # dict(list(context.items()) + list(c_def.items()))

    # Выбрать что именно отображать, тут случай с чекером published
    def get_queryset(self):
        # select_related - загрузка связанных данных по ForeignKey для оптимизации SQL-запросов
        return Post.objects.filter(is_published=True).select_related('cat')


# Категории
class PostCategory(DataMixin, ListView):
    model = Post
    template_name = 'info/index.html'
    context_object_name = 'posts'  # Указывает имя для переменной в index.html
    allow_empty = False  # Для вызова 404 при несуществующем URL-slug

    # Отображение "внутренностей", меню
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return context | c_def

    # Обращаемся к параметру slug из таблицы cat и select_related - загрузка данных по key (см. коммент в PostHome)
    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')


# Отображение поста(Читать пост)
class ShowPost(DataMixin, DetailView):
    model = Post
    template_name = 'info/post.html'
    slug_url_kwarg = 'post_slug'  # для id, pk_url_slug
    context_object_name = 'post'  # отображаем пост(в переменную post в post.html)

    # Функция отображения "внутренностей", меню
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return context | c_def


def about(request):
    return render(request, 'info/about.html', {'title': 'О сайте'})


# "Добавить статью", отображение страницы и связь с формой
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'info/add_page.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    # Функция отображения "внутренностей", меню
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return context | c_def


def contact(request):
    return render(request, 'info/contact.html', {'title': 'Контакты'})


def PageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена.</h1>')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'info/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return context | c_def

    # Вызывается при успешной проверки формы регистрации и сразу авторизует юзера после регистрации
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'info/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
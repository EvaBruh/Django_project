from django import template
from info.models import *
from info.views import menu

register = template.Library()


@register.simple_tag(name='getcats') # простой тег; возвращаем коллекцию данных и используем в шаблоне base.html
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('info/list_menu.html') # включающий тег с передачей ему переменных из base.html
def show_menu():
    return {'menu': menu}


@register.inclusion_tag('info/list_categories.html') # включающий тег с передачей ему переменных из base.html
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats, 'cat_selected': cat_selected}


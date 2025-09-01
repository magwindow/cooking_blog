from django.shortcuts import render
from .models import Category, Post


def index(request):
    """Для главной страницы"""
    posts = Post.objects.all()  # SELECT * FROM post
    context = {
        'title': 'Главная страница',
        'posts': posts
    }
    return render(request, 'cooking/index.html', context)

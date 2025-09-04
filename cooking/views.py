from django.db.models import F
from django.shortcuts import render
from .models import Post


def index(request):
    """Для главной страницы"""
    posts = Post.objects.all()  # SELECT * FROM post
    context = {
        'title': 'Главная страница',
        'posts': posts
    }
    return render(request, 'cooking/index.html', context)


def category_list(request, pk):
    """Реакция на нажатие кнопки категории"""
    posts = Post.objects.filter(category_id=pk)
    context = {
        'title': posts[0].category,
        'posts': posts
    }
    return render(request, 'cooking/index.html', context)


def post_detail(request, pk):
    """Страница статьи"""
    article = Post.objects.get(pk=pk)
    Post.objects.filter(pk=pk).update(watched=F('watched') + 1)
    ext_post = Post.objects.all().order_by('-watched')[:5]
    context = {
        'title': article.title,
        'post': article,
        'ext_posts': ext_post
    }
    return render(request, 'cooking/article_detail.html', context)
from django.db.models import F
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages

from .models import Post
from .forms import PostAddForm, LoginForm, RegistrationForm


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
    ext_post = Post.objects.all().exclude(pk=pk).order_by('-watched')[:5]
    context = {
        'title': article.title,
        'post': article,
        'ext_posts': ext_post
    }
    return render(request, 'cooking/article_detail.html', context)


def add_post(request):
    """Добавление статьи от пользователя, без админки"""
    if request.method == 'POST':
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(**form.cleaned_data)
            post.save()
            return redirect('post_detail', post.pk)
    else:
        form = PostAddForm()

    context = {
        'form': form,
        'title': 'Добавить статью'
    }
    return render(request, 'cooking/article_add_form.html', context)


def user_login(request):
    """Аутентификация пользователя"""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в аккаунт!')
            return redirect('index')
    else:
        form = LoginForm()

    context = {
        'title': 'Авторизация пользователя',
        'form': form
    }
    return render(request, 'cooking/login_form.html', context)


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect('index')


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {
        'title': 'Регистрация пользователя',
        'form': form
    }
    return render(request, 'cooking/register.html', context)
from django.db.models import F, Q
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .models import Post, Category, Comment
from .forms import PostAddForm, LoginForm, RegistrationForm, CommentForm


class Index(ListView):
    """Для главной страницы"""
    model = Post
    context_object_name = 'posts'
    template_name = 'cooking/index.html'
    extra_context = {'title': 'Главная страница'}


class ArticleByCategory(Index):
    """Реакция на нажатие кнопки категории"""

    def get_queryset(self):
        """Здесь можем переделать фильтрацию"""
        return Post.objects.filter(category_id=self.kwargs['pk'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        """Для динамических данных"""
        context = super().get_context_data()  # context = {}
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = category
        return context


class PostDetail(DetailView):
    """Страница статьи"""
    model = Post
    template_name = 'cooking/article_detail.html'

    def get_queryset(self):
        """Здесь можем переделать фильтрацию"""
        return Post.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        """Для динамических данных"""
        Post.objects.filter(pk=self.kwargs['pk']).update(watched=F('watched') + 1)
        context = super().get_context_data()
        post = Post.objects.get(pk=self.kwargs['pk'])
        posts = Post.objects.all().exclude(pk=self.kwargs['pk']).order_by('-watched')[:5]
        context['title'] = post
        context['ext_posts'] = posts
        context['comments'] = Comment.objects.filter(post=post)

        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm
        return context


class AddPost(CreateView):
    """Добавление статьи от пользователя, без админки"""
    form_class = PostAddForm
    template_name = 'cooking/article_add_form.html'
    extra_context = {'title': 'Добавить статью'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(UpdateView):
    """Изменение статьи по кнопке"""
    model = Post
    form_class = PostAddForm
    template_name = 'cooking/article_add_form.html'


class PostDelete(DeleteView):
    """Удаление статьи по кнопке"""
    model = Post
    success_url = reverse_lazy('index')
    context_object_name = 'post'
    extra_context = {'title': 'Изменить статью'}


class SearchResult(Index):
    """Поиск слова в заголовках и содержании статьи"""
    def get_queryset(self):
        """Функция для фильтрации выборок из db"""
        word = self.request.GET.get('q')
        posts = Post.objects.filter(
            Q(title__icontains=word) | Q(content__icontains=word)
        )
        return posts


def add_comment(request, post_id):
    """Добавление комментарии к статьям"""
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = Post.objects.get(pk=post_id)
        comment.save()

    return redirect('post_detail', post_id)


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


def profile(request, user_id):
    """Страница пользователя"""
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(author=user)
    context = {
        'user': user,
        'posts': posts
    }
    return render(request, 'cooking/profile.html', context)

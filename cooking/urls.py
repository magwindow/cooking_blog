from django.urls import path
from .views import *

urlpatterns = [
    # Маршруты на базе классов
    path('', Index.as_view(), name='index'),
    path('category/<int:pk>/', ArticleByCategory.as_view(), name='category_list'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('add_article/', AddPost.as_view(), name='add'),
    path('post/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    # Маршруты на базе функции
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
]
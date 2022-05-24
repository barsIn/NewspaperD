from django.contrib import admin
from django.urls import path, include
from .views import NewsView, NewView, NewsSearch, NewsCreate, CategoryCreate, CategoryView, NewsUpdate, NewsDelete, AuthorView, AuthorUpdate, UserUpdate, UserView, upgrade_me

urlpatterns = [
    path('', NewsView.as_view()),
    path('<int:pk>', NewView.as_view()),
    path('search', NewsSearch.as_view()),
    path('create', NewsCreate.as_view(), name='news_create'),
    path('create/category', CategoryCreate.as_view(), name='category_create'),
    path('category/<int:pk>', CategoryView.as_view(), name='categorys'),
    path('<int:pk>/edit', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
    path('author/<int:pk>', AuthorView.as_view(), name='author'),
    path('author/<int:pk>/edit', AuthorUpdate.as_view(), name='author_update'),
    path('user/<int:pk>/edit', UserUpdate.as_view(), name='user_update'),
    path('user/<int:pk>', UserView.as_view(), name='user'),
    path('accounts/', include('allauth.urls')),
    path('user/upgrade/', upgrade_me, name='userupgrade'),
]
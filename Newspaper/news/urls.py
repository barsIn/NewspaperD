from django.contrib import admin
from django.urls import path, include
from .views import NewsView, NewView, NewsSearch, NewsCreate, CategoryCreate, CategoryView, NewsUpdate, NewsDelete

urlpatterns = [
    path('', NewsView.as_view()),
    path('<int:pk>', NewView.as_view()),
    path('search', NewsSearch.as_view()),
    path('create', NewsCreate.as_view(), name='news_create'),
    path('create/category', CategoryCreate.as_view(), name='category_create'),
    path('category/<int:pk>', CategoryView.as_view(), name='categorys'),
    path('<int:pk>/edit', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
]
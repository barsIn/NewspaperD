from django.contrib import admin
from django.urls import path, include
from .views import NewsView, NewView

urlpatterns = [
    path('', NewsView.as_view()),
    path('<int:pk>', NewView.as_view())
]
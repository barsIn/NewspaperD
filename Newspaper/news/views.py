from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

class NewsView(ListView):
    model = Post
    ordering = 'publication_date'
    template_name = 'news.html'
    context_object_name = 'news'


class NewView(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'



# Create your views here.

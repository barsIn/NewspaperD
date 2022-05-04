from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm, CategoryForm

class NewsView(ListView):
    model = Post
    ordering = 'publication_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class NewView(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class CategoryView(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'


class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 5
    ordering = ['rating']

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):

        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
        }

class NewsCreate(CreateView):
    template_name = 'news_create.html'
    form_class = PostForm

class CategoryCreate(CreateView):
    template_name = 'category_create.html'
    form_class = CategoryForm

class NewsUpdate(UpdateView):
    template_name = 'news_create.html'
    form_class = PostForm


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    context_object_name = 'new'





# Create your views here.

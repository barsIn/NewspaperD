from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category, Author, User
from .filters import PostFilter
from .forms import PostForm, CategoryForm, AuthorForm, UserForm

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

class NewsCreate(LoginRequiredMixin, CreateView):
    template_name = 'news_create.html'
    form_class = PostForm

class CategoryCreate(LoginRequiredMixin, CreateView):
    template_name = 'category_create.html'
    form_class = CategoryForm

class NewsUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'news_update.html'
    form_class = PostForm
    model = Post
    context_object_name = 'new'


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    context_object_name = 'new'


class AuthorView(DetailView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'author'


class AuthorUpdate(LoginRequiredMixin, UpdateView):
    form_class = AuthorForm
    template_name = 'author_update.html'
    model = Author
    context_object_name = 'author'

class UserUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    template_name = 'user_update.html'
    model = User
    context_object_name = 'user'

class UserView(DetailView):
    model = User
    template_name = 'user.html'
    context_object_name = 'user'





# Create your views here.

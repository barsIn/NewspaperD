from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post, Category, Author, User
from .filters import PostFilter
from .forms import PostForm, CategoryForm, AuthorForm, UserForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


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


class NewsCreate(PermissionRequiredMixin, CreateView):
    template_name = 'news_create.html'
    form_class = PostForm
    permission_required = ('news.add_post')
    permission_denied_message = 'У Вас недостаточно прав'


class CategoryCreate(PermissionRequiredMixin, CreateView):
    template_name = 'category_create.html'
    form_class = CategoryForm
    permission_required = ('news.add_category')
    permission_denied_message = 'У Вас недостаточно прав'


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'news_update.html'
    form_class = PostForm
    model = Post
    context_object_name = 'new'
    permission_required = ('news.change_post')
    permission_denied_message = 'У Вас недостаточно прав'


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    context_object_name = 'new'


class AuthorView(LoginRequiredMixin, DetailView):
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


class UserView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        # context['author'] = Author.objects.filter(user.user)
        context['author'] = Author.objects.filter(user=self.request.user).exists()

        return context


@login_required
def upgrade_me(request):
    user = request.user

    if Author.objects.filter(user=user).exists():
        author1 = Author.objects.get(user=user)
        id = author1.id
        return redirect(f'/news/author/{id}')
    else:
        author_group = Group.objects.get(name='authors')
        author_group.user_set.add(user)
        author1 = Author.objects.create(user=user)
        id = author1.id
    return redirect(f'/news/author/{id}')




# Create your views here.

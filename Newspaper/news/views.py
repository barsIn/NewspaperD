from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post, Category, Author, User
from .filters import PostFilter
from .forms import PostForm, CategoryForm, AuthorForm, UserForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
from .tasks import hello, printer
from django.views import View
from datetime import datetime, timedelta
from django.core.cache import cache
import logging
from django.utils.translation import gettext as _
from django.utils import timezone
from django.shortcuts import redirect
import pytz

load_dotenv()
logger = logging.getLogger(__name__)


class Index(View):
    def get(self, request):
        string = _('Hello world')

        return HttpResponse(string)


class IndexView(View):
    def get(self, request):
        hello.delay()
        printer.apply_async([10],
                            eta=datetime.now() + timedelta(seconds=5),
                            expires=datetime.now() + timedelta(seconds=8))
        string = _('Hello')
        return HttpResponse(string)


class NewsView(ListView):
    model = Post
    ordering = '-publication_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class NewView(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    curent_time = timezone.now()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timezones'] = pytz.common_timezones
        context['current_time'] = timezone.now()
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')



    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно

        obj = cache.get(f'product-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = self.requequest.user
        # category = self.get_object().category.all()
        context['categorys'] = self.get_object().category.all()
        context['user'] = self.request.user
        return context


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
    permission_denied_message = _('Permission denied')

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.author = Author.objects.get(user=self.request.user)
        fields.save()
        return super().form_valid(form)

        # def post(self, request, *args, **kwargs):
        #     form = self.form_class(request.POST)
        #     if form.is_valid():
        #         self.form_valid(form)
        #         form.save()
        #     heading = request.POST['post_heading']
        #     post_body = request.POST['post_text']
        #     category = request.POST.getlist('category')
        #     user = self.request.user
        #     for id in category:
        #         categ = Category.objects.get(id=id)
        #         subscribers = categ.user.all()
        #         id = len(Post.objects.all())
        #         print(f'Вот номер id {id}')
        #
        #         if subscribers.exists():
        #
        #             for sub in subscribers:
        #
        #                 html_content = render_to_string(
        #                     'subs_sent.html',
        #                     {
        #                         'user': sub,
        #                         'heading': heading,
        #                         'post': post_body,
        #                         'category': categ.category_name,
        #                         'post_id': id,
        #                     }
        #                 )
        #                 msg = EmailMultiAlternatives(
        #                     subject='Hello from news portal',
        #                     body=f'Новая новость в категории {categ}',  # это то же, что и message
        #                     from_email=os.getenv('MY_MAIL'),
        #                     to=[sub.email],  # это то же, что и recipients_list
        #                 )
        #                 msg.attach_alternative(html_content, "text/html")
        #                 msg.send()
        # send_mail(
        #     subject=f'{categ} {user}',
        #     # имя клиента и дата записи будут в теме для удобства
        #     message=f'Новая новость в категории {categ}',  # сообщение с кратким описанием проблемы
        #     from_email=os.getenv('MY_MAIL'),
        #     # здесь указываете почту, с которой будете отправлять (об этом попозже)
        #     recipient_list=[sub.email]  # здесь список получателей. Например, секретарь, сам врач и т. д.
        # )

        return redirect('/news/')


class CategoryCreate(PermissionRequiredMixin, CreateView):
    template_name = 'category_create.html'
    form_class = CategoryForm
    permission_required = ('news.add_category')
    permission_denied_message = _('Permission denied')


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'news_update.html'
    form_class = PostForm
    model = Post
    context_object_name = 'new'
    permission_required = ('news.change_post')
    permission_denied_message = _('Permission denied')

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


@login_required
def subscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    if user in category.user.all():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        category.user.add(user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def unsubscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    if user in category.user.all():
        category.user.remove(user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class CategorySubscribe(LoginRequiredMixin, UpdateView):
    pass

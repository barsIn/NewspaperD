from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy



class Post(models.Model):
    POST_CHOICES = [
        ('NW', 'Новость'),
        ('PS', 'Статья'),
    ]

    post_heading = models.CharField(max_length=64, help_text=_('post heading'))
    post_text = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    changepublication_date = models.DateTimeField(auto_now=True)
    post_type = models.CharField(max_length=2,
                                 choices=POST_CHOICES,
                                 default='NW')

    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='author', verbose_name=pgettext_lazy('help text for author', 'This is the help text'),)
    category = models.ManyToManyField('Category', through='PostCategory', blank=True, related_name='category')

    def __str__(self):
        return f'{self.post_heading.title()} популярный пост, его рейтинг {self.rating}, категории {self.category.all()}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        preview_text = self.post_text[0:124] + '...'
        return preview_text


class Author(models.Model):
    author_rating = models.IntegerField(default=0)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_online = models.DateTimeField(auto_now=True)
    is_autor_online = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Автор {self.user.username}'

    def get_absolute_url(self):
        return f'/news/author/{self.id}'

    def update_rating(self):
        posts_rating = 0
        comments_rating = 0
        posts_coments_rating = 0
        author_posts = self.post_set.all()
        if author_posts.exists():
            for post in author_posts:
                posts_rating += post.rating
                for comment in post.comment_set.all():
                    posts_coments_rating += comment.comment_rating
        author_user = self.user
        author_comments = author_user.comment_set.all()
        if author_comments.exists():
            for i in author_comments:
                comments_rating += i.comment_rating
        self.author_rating = posts_rating * 3 + comments_rating + posts_coments_rating
        self.save()


class Comment(models.Model):
    comment_text = models.TextField()
    comment_rating = models.IntegerField()
    create_comment_time = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)

    user = models.ManyToManyField(User, blank=True, related_name='users_of_category')

    def __str__(self):
        return f'{self.category_name}'

    def get_absolute_url(self):
        return f'/news/category/{self.id}'


class PostCategory(models.Model):
    news = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    POST_CHOICES = [
        ('NW', 'Новость'),
        ('PS', 'Статья'),
    ]

    post_heading = models.CharField(max_length=64)
    post_text = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    changepublication_date = models.DateTimeField(auto_now=True)
    post_type = models.CharField(max_length=2,
                                 choices=POST_CHOICES,
                                 default='NW')

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    category = models.ManyToManyField('Category', through='PostCategory', blank=True)

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


class PostCategory(models.Model):
    news = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

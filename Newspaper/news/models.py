from django.db import models


class News (models.Model):
    news_heading = models.CharField(max_length=64)
    news_text = models.TextField()
    ppublication_date = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField()

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    category = models.ManyToManyField('Category', through='NewsCategory')


class Author (models.Model):
    author_nikname = models.CharField(max_length=32)
    author_emale = models.EmailField(null=True)
    author_rating = models.IntegerField(default=0)


class User (models.Model):
    pass


class Comment (models.Model):
    comment_text = models.TextField()
    comment_likes = models.IntegerField()

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)


class Category (models.Model):
    category_name = models.CharField(max_length=64)


class NewsCategory(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


from django.contrib import admin
from .models import User, Author, Comment, Post, Category, PostCategory



admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)


# Register your models here.

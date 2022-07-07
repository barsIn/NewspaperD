from django.contrib import admin
from .models import User, Author, Comment, Post, Category, PostCategory
from .translation import PostTranslationOptions, CategoryTranslationOptions, CommentTranlationOptions
from modeltranslation.admin import TranslationAdmin



def nullfy_rating(modeladmin, request, queryset): #
    queryset.update(rating=0)
nullfy_rating.short_description = 'Обнулить рейтинг'


# class PostAdmin(admin.ModelAdmin):
#     # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
#     list_display = ['post_heading', 'rating', 'author'] # генерируем список имён всех полей для более красивого отображения
#     list_filter = ('author', 'post_type', 'publication_date')  # добавляем примитивные фильтры в нашу админку
#     search_fields = ('publication_date', 'category__name')  # тут всё очень похоже на фильтры из запросов в базу
#     actions = [nullfy_rating]


class PostAdmin(TranslationAdmin):
    model = Post

class CategoryAdmin(TranslationAdmin):
    model = Category

class CommentAdmin(TranslationAdmin):
    model = Comment


admin.site.register(Author)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory)


# Register your models here.

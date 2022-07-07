from .models import Post, Category, Comment
from modeltranslation.translator import register, TranslationOptions


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('post_heading', 'post_text', 'post_type')  # указываем, какие именно поля надо переводить в виде кортежа


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(Comment)
class CommentTranlationOptions(TranslationOptions):
    fields = ('comment_text',)
from django.forms import ModelForm, BooleanField
from .models import Post, Category


# Создаём модельную форму
class PostForm(ModelForm):
    check_box = BooleanField(label='Я принимаю условия соглашения')

    class Meta:
        model = Post
        fields = ['post_heading','post_text', 'post_type', 'author', 'category']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']
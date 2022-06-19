from django.forms import ModelForm, BooleanField
from .models import Post, Category, Author, User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


# Создаём модельную форму
class PostForm(ModelForm):
    check_box = BooleanField(label='Я принимаю условия соглашения')


    class Meta:
        model = Post
        fields = ['post_heading', 'post_text', 'post_type', 'category']




class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['author_rating']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ModersSignupForm(SignupForm):

    def save(self, request):
        user = super(ModersSignupForm, self).save(request)
        moders_group = Group.objects.get(name='moders')
        moders_group.user_set.add(user)
        return user


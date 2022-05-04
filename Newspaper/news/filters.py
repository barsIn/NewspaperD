from django.template.backends import django
from django_filters import FilterSet, DateFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):
    class Meta:
        publication_date = DateFilter(
            lookup_expr='gt',
            widget=forms.DateInput(
                attrs={
                    'type': 'date'
                }
            )
        )

        model = Post

        fields = {'post_heading': ['icontains'],
                  'author': ['exact'],
                  'category__category_name': ['icontains'],



                  'publication_date': ['gt', 'lt'],

                  # 'category': ['exact']
                  }

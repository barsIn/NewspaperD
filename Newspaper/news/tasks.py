from celery import shared_task
import time, os
from dotenv import load_dotenv

from datetime import datetime, timedelta
from .models import Post, Category
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

load_dotenv()


@shared_task
def hello():
    time.sleep(10)
    print('Hello world!')


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i + 1)


@shared_task
def category_send():
    lat_time = datetime.now() - timedelta(weeks=1)
    categorys = set()
    subs = set()
    news = Post.objects.filter(publication_date__gte=lat_time)
    sub_posts = set()
    if news.exists():
        for new in news:
            news_categorys = new.category.all()
            for cat in news_categorys:
                categorys.add(cat)
    if len(categorys) > 0:
        for cat in categorys:
            cat_sub = cat.user.all()
            for sub in cat_sub:
                subs.add(sub)
    if len(subs) > 0:
        for sub in subs:
            sub_categorys = Category.objects.filter(user=sub)
            for cat in sub_categorys:
                posts = Post.objects.filter(category=cat)
                for post in posts:
                    sub_posts.add(post)
            html_content = render_to_string(
                'weekly_sent.html',
                {
                    'user': sub,
                    'news': sub_posts,
                    'category': sub_categorys,

                }
            )
            msg = EmailMultiAlternatives(
                subject='Hello from news portal',
                body=f'Новые новости за неделю в категори(ях) {sub_categorys}',  # это то же, что и message
                from_email=os.getenv('MY_MAIL'),
                to=[sub.email],  # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            sub_posts.clear()


@shared_task
def new_post_created(cat, email, name, post_heading, post_text, id):
    html_content = render_to_string(
            'subs_sent.html',
            {
                'user': name,
                'heading': post_heading,
                'post': post_text,
                'category': cat,
                'post_id': id,
            }
        )
    msg = EmailMultiAlternatives(
        subject='Hello from news portal',
        body=f'Новая новость в категории {cat}',  # это то же, что и message
        from_email=os.getenv('MY_MAIL'),
        to=[email],  # это то же, что и recipients_list
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

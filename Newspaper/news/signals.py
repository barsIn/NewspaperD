from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from dotenv import load_dotenv
import os
from .models import Post, Category
from .tasks import new_post_created

load_dotenv()


@receiver(m2m_changed, sender=Post.category.through)
def subscribers_mailing(sender, instance, action, **kwargs):

    subers = []
    if action == 'post_add':
        for cat in instance.category.all():
            for sub in cat.user.all():
                subers.append(sub)
            for user in subers:
                # html_content = render_to_string(
                #     'subs_sent.html',
                #     {
                #         'user': user,
                #         'heading': instance.post_heading,
                #         'post': instance.post_text,
                #         'category': cat,
                #         'post_id': instance.id,
                #     }
                # )

                # msg = EmailMultiAlternatives(
                #     subject='Hello from news portal',
                #     body=f'Новая новость в категории {cat}',  # это то же, что и message
                #     from_email=os.getenv('MY_MAIL'),
                #     to=[user.email],  # это то же, что и recipients_list
                # )

                # msg.attach_alternative(html_content, "text/html")
                new_post_created.delay([cat, user.email, user.username, instance.post_heading, instance.post_text, instance.id])


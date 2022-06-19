import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.mail import EmailMultiAlternatives
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from news.models import Post, Category

load_dotenv()

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    print('Работает задача')
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



    #  Your job processing logic here...



# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(minute="*/2"),
            # trigger=CronTrigger(day_of_week="mon"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
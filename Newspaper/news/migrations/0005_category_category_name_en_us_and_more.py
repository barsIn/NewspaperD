# Generated by Django 4.0.3 on 2022-07-06 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_name_en_us',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='category_name_ru',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_text_en_us',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_text_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_heading_en_us',
            field=models.CharField(help_text='заголовок поста', max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_heading_ru',
            field=models.CharField(help_text='заголовок поста', max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_text_en_us',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_text_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_type_en_us',
            field=models.CharField(choices=[('NW', 'Новость'), ('PS', 'Статья')], default='NW', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_type_ru',
            field=models.CharField(choices=[('NW', 'Новость'), ('PS', 'Статья')], default='NW', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='news.author', verbose_name='This is the help text'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_heading',
            field=models.CharField(help_text='заголовок поста', max_length=64),
        ),
    ]

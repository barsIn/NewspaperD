from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Необходимо ввести название категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no ')

        if answer != 'yes' or 'y':
            self.stdout.write(self.style.ERROR('Отменено'))
        else:
            try:
                category = Category.objects.get(category_name=options['category'])
                Post.objects.filter(category == category).delete()
                self.stdout.write(self.style.SUCCESS(
                    f'Succesfully deleted all news from category {category.category_name}'))
            except Post.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Could not find category {options['category']}"))


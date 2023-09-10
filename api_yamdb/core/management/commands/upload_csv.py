import csv
import os
from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from reviews.models import Category, Comment, Genre, Review, Title, TitlesGenre
from users.models import User


class Command(BaseCommand):
    help = u'Перенос csv таблицы в бд'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'dir', type=str, help=u'Укажите полный путь к папке'
        )

    def create_data(self, dr, model):
        models = []
        data = [(i) for i in dr]
        for i in range(len(data)):
            models.append(model(**data[i]))
        print(model.objects.bulk_create(models))

    def handle(self, *args: Any, **options: Any):
        try:
            dir = options.get('dir')

            for filename in os.listdir(dir):
                with open(
                    os.path.join(dir, filename),
                    'r',
                    encoding='UTF-8',
                ) as fl:
                    dr = csv.DictReader(fl)
                    if filename == '2. category.csv':
                        self.create_data(dr, Category)
                    elif filename == '3. genre.csv':
                        self.create_data(dr, Genre)
                    elif filename == '4. titles.csv':
                        self.create_data(dr, Title)
                    elif filename == '5. genre_title.csv':
                        self.create_data(dr, TitlesGenre)
                    elif filename == '7. comments.csv':
                        self.create_data(dr, Comment)
                    elif filename == '6. review.csv':
                        self.create_data(dr, Review)
                    elif filename == '1. users.csv':
                        self.create_data(dr, User)

        except Exception as error:
            print(f'Что-то пошло не так: {error}')

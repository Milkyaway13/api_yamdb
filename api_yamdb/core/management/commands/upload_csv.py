import csv
import os
from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from users.models import User

from titles.models import (
    Categories,
    Comments,
    Genres,
    Reviews,
    Titles,
    TitlesGenre,
)


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

    def handle(self, *args: Any, **options: Any) -> str | None:
        try:
            dir = options.get('dir')

            for filename in os.listdir(dir):
                with open(
                    os.path.join(dir, filename),
                    'r',
                    encoding='UTF-8',
                ) as fl:
                    dr = csv.DictReader(fl)
                    if filename == 'category.csv':
                        self.create_data(dr, Categories)
                    elif filename == 'genre.csv':
                        self.create_data(dr, Genres)
                    elif filename == 'titles.csv':
                        self.create_data(dr, Titles)
                    elif filename == 'genre_title.csv':
                        self.create_data(dr, TitlesGenre)
                    elif filename == 'comments.csv':
                        self.create_data(dr, Comments)
                    elif filename == 'review.csv':
                        self.create_data(dr, Reviews)
                    elif filename == 'users.csv':
                        self.create_data(dr, User)

        except Exception as error:
            print(f'Что-то пошло не так: {error}')

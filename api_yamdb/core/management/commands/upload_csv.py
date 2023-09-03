from typing import Any
from django.core.management.base import BaseCommand, CommandParser
import csv, sqlite3, os
from titles.models import Categories, Genres, Titles


class Command(BaseCommand):
    help = u'Перенос csv таблицы в бд'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('path', type=str, help=u'полный путь к csv файлу')

    def create_data(self, dr, model):
        data = [(i) for i in dr]
        for i in range(len(data)):
            model.objects.create(**data[i])
        print(data)

    def handle(self, *args: Any, **options: Any) -> str | None:
        path = options.get('path')

        try:
            with open(path, 'r', encoding='UTF-8') as fl:
                dr = csv.DictReader(fl)
                if os.path.basename(fl.name) == 'category.csv':
                    self.create_data(dr, Categories)
                elif os.path.basename(fl.name) == 'genres.csv':
                    self.create_data(dr, Genres)
                elif os.path.basename(fl.name) == 'titles.csv':
                    self.create_data(dr, Titles)

        except Exception as error:
            print(f'Проверьте правильность введенных данных: {error}')

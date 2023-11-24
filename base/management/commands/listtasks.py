#zadanie 7 1 management команда
from django.core.management.base import BaseCommand
from base.models import Task

class Command(BaseCommand):
    help = 'List all tasks in the database'

    def handle(self, *args, **options):
        # Получаем все задачи из базы данных
        tasks = Task.objects.all()

        # Проходимся по каждой задаче и выводим информацию о ней
        for task in tasks:
            # Используем self.stdout.write для вывода в консоль
            self.stdout.write((f'Task: {task.title}, User: {task.user}, Complete: {task.complete}'))
#python manage.py listtasks
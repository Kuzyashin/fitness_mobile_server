from django.core.management.base import BaseCommand
from project.applications.lessons.models import Lesson
from project.applications.lessons.utils.parser import get_data


class Command(BaseCommand):
    help = 'Get initial data'

    def handle(self, *args, **options):
        Lesson.objects.all().delete()
        data = get_data()
        for lesson in data:
            Lesson.objects.create(**lesson)

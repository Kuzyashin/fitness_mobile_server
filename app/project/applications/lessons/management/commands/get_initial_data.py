from django.core.management.base import BaseCommand
from lessons.models import Lesson
from lessons.utils.parser import get_data


class Command(BaseCommand):
    help = 'Get initial data'

    def handle(self, *args, **options):
        Lesson.objects.all().delete()
        data = get_data()
        for lesson in data:
            Lesson.objects.create(**lesson)

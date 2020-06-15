from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

# Create your views here.
from project.applications.lessons.models import Lesson
from project.applications.lessons.serializers import LessonSerializer


class LessonViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

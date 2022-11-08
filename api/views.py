import random
import string

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponse
from rest_framework import generics
from rest_framework.response import Response

from .models import Title, Tags, Volume, Chapter
from .serializers import TitleSerializer, SingleTitleSerializer, TagsSerializer, VolumeSerializer, ChapterSerializer
from .pagination import LargeResultsSetPagination
from .tasks import increase_view, increase_like


def add_test_titles(request, count):
    """Добавляет рандомные Title в бд"""
    for _ in range(int(count)):
        Title.objects.create(
            ru_name=''.join(random.sample(string.ascii_letters, 20)),
            en_name=''.join(random.sample(string.ascii_letters, 20)),
            alt_name=''.join(random.sample(string.ascii_letters, 20)) if random.randint(0, 1) else None,
            description=''.join(random.sample(string.ascii_letters, 20)) if random.randint(0, 1) else ''
        )
    return HttpResponse('OK')


def add_test_tags(request, count):
    """Добавляет рандомные Tags в бд"""
    for _ in range(int(count)):
        Tags.objects.create(
            tag_name=''.join(random.sample(string.ascii_letters, 30))
        )
    return HttpResponse('OK')


# Create your views here.
class TagView(generics.ListAPIView):
    """API GET: List of Tags"""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = LargeResultsSetPagination


class VolumeView(generics.ListAPIView):
    """API GET: List of Volumes, contains Chapters"""
    queryset = Volume.objects.all()
    serializer_class = VolumeSerializer
    pagination_class = LargeResultsSetPagination


class ChapterView(generics.ListAPIView):
    """API GET: List of Chapters"""
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    pagination_class = LargeResultsSetPagination


class SingleChapterView(generics.RetrieveAPIView, generics.CreateAPIView):
    """ API
    GET: Chapter by pk, increase chapter_view_count by 1
    POST: Increase chapter_likes_count by 1
    """
    queryset = Chapter.objects.filter()
    serializer_class = ChapterSerializer

    def get(self, request, pk, *args, **kwargs):
        try:
            queryset = Chapter.objects.get(pk=pk)
            serializer = ChapterSerializer(queryset, many=False)
            increase_view.delay(pk)
            message = 'OK'
            response_data = serializer.data
        except ObjectDoesNotExist:
            message = 'Chapter not exists'
            response_data = {}
        except Exception:
            message = 'Internal server error'
            response_data = {}

        return Response({
            'message': message,
            'data': response_data
        })

    def post(self, request, pk, *args, **kwargs):
        try:
            Chapter.objects.get(pk=pk)
            increase_like.delay(pk)
            message = "OK"
        except ObjectDoesNotExist:
            message = 'Chapter not exists'
        except Exception:
            message = 'Internal server error'

        return Response({
            'message': message,
        })


class TitleView(generics.ListAPIView):
    """API
    GET: List of Titles
    GET PAGINATION: key=per_page, default=20, max_per_page=50
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LargeResultsSetPagination


class SingeTitleView(generics.RetrieveAPIView):
    """ API GET: Title by pk, contains Volumes"""
    queryset = Title.objects.filter()
    serializer_class = SingleTitleSerializer



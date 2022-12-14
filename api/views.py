import random
import string

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponse
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import generics
from rest_framework.response import Response

from .models import Title, Tags, Volume, Chapter
from .serializers import TitleSerializer, SingleTitleSerializer, TagsSerializer, VolumeSerializer, ChapterSerializer, \
    SingleChapterGetSerializer, SingleChaprerGetErrorSerializer, ChapterResponseLikeSerializer, ChapterPostLikeSerializer
from .pagination import LargeResultsSetPagination
from .tasks import increase_view, increase_like
from .test_data import create_test_items, create_random_titles, create_random_tags


def add_test_titles(request, count):
    """Добавляет рандомные Title в бд"""
    create_random_titles(count)
    return HttpResponse('OK')


def add_test_tags(request, count):
    """Добавляет рандомные Tags в бд"""
    create_random_tags(count)
    return HttpResponse('OK')


def add_test_data(request):
    """Добавляет тестовые данные в бд"""
    create_test_items()
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

    GET_404_MESSAGE = 'Chapter not exists'
    GET_500_MESSAGE = 'Internal server error'
    GET_ERROR_DATA = {}

    @swagger_auto_schema(
        operation_id='single chapter',
        operation_description='Get Chapter by pk, increase chapter_view_count by 1',
        tags=['chapters', ],
        responses={
            '200': SingleChapterGetSerializer(),
            '404': SingleChaprerGetErrorSerializer(),
            '500': SingleChaprerGetErrorSerializer(),
        }

    )
    def get(self, request, pk, *args, **kwargs):
        try:
            queryset = Chapter.objects.get(pk=pk)
            serializer = ChapterSerializer(queryset, many=False)
            increase_view.delay(pk)
            message = 'OK'
            response_data = serializer.data
            status_code = 200
        except ObjectDoesNotExist:
            message = self.GET_404_MESSAGE
            response_data = self.GET_ERROR_DATA
            status_code = 404
        except Exception:
            message = self.GET_500_MESSAGE
            response_data = self.GET_ERROR_DATA
            status_code = 500

        return Response({
            'message': message,
            'data': response_data
        }, status=status_code)

    @swagger_auto_schema(
        tags=['likes', ],
        operation_id='add like',
        operation_description='POST: Increase chapter_likes_count by 1',
        query_serializer=ChapterPostLikeSerializer(),
        responses={
            '200': ChapterResponseLikeSerializer(),
            '404': ChapterResponseLikeSerializer(),
            '500': ChapterResponseLikeSerializer(),
        },
        request_body=no_body,
    )
    def post(self, request, pk, *args, **kwargs):
        try:
            Chapter.objects.get(pk=pk)
            increase_like.delay(pk)
            message = "OK"
            status = 200
        except ObjectDoesNotExist:
            message = 'Chapter not exists'
            status = 404
        except Exception:
            message = 'Internal server error'
            status = 500

        return Response({
            'message': message,
        }, status=status)


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

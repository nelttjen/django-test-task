from django.urls import path, include, re_path

from django_test_task.settings import DEBUG
from .views import TitleView, SingeTitleView, ChapterView, SingleChapterView

API_ENDPOINT = 'api/v1/'

urlpatterns = [
    re_path(r'titles/(?P<pk>\d+)/', SingeTitleView.as_view(), name='single_title_view'),
    re_path(r'titles/', TitleView.as_view(), name='title_view'),
    re_path(r'chapters/(?P<pk>\d+)/', SingleChapterView.as_view(), name='single_chapter_view'),
    re_path(r'chapters/', ChapterView.as_view(), name='chapter_view'),
]

if DEBUG:
    from .views import add_test_titles, add_test_tags, add_test_data
    urlpatterns = [
        re_path(r'add_titles/(?P<count>\d+)', add_test_titles),
        re_path(r'add_tags/(?P<count>\d+)', add_test_tags),
        re_path(r'test_items/', add_test_data)
    ] + urlpatterns

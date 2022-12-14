from django.urls import path, include, re_path

from django_test_task.settings import DEBUG
from .views import TitleView, SingeTitleView, ChapterView, SingleChapterView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

API_ENDPOINT = 'api/v1/'

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

yasg_patterns = [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


urlpatterns = [
    re_path(r'titles/(?P<pk>\d+)/', SingeTitleView.as_view(), name='single_title_view'),
    re_path(r'titles/', TitleView.as_view(), name='title_view'),
    re_path(r'chapters/(?P<pk>\d+)/', SingleChapterView.as_view(), name='single_chapter_view'),
    re_path(r'chapters/', ChapterView.as_view(), name='chapter_view'),
] + yasg_patterns

if DEBUG:
    from .views import add_test_titles, add_test_tags, add_test_data
    urlpatterns = [
        re_path(r'add_titles/(?P<count>\d+)', add_test_titles),
        re_path(r'add_tags/(?P<count>\d+)', add_test_tags),
        re_path(r'test_items/', add_test_data)
    ] + urlpatterns

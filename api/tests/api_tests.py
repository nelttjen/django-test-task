import time

from django.urls import resolve, reverse
from django.test import TestCase, override_settings
from rest_framework.test import RequestsClient

from api.views import TitleView, SingeTitleView, ChapterView, SingleChapterView
from api.models import Title, Tags, Volume, Chapter
from api.tasks import increase_view, increase_like

# Create your tests here.
base_endpoint = 'http://127.0.0.1:8000/api/v1/'
client = RequestsClient()


class DBTestItemsDefault:
    def create_test_db_items(self):
        self.title1 = Title.objects.create(
            ru_name='Тайтл 1',
            en_name='Title 1',
            description='Title 1 desc'
        )
        self.tag1 = Tags.objects.create(
            tag_name='Tag 1'
        )
        self.tag2 = Tags.objects.create(
            tag_name='Tag 2'
        )
        self.title2 = Title.objects.create(
            ru_name='Тайтл 2 с тегами',
            en_name='Title 2 with tags',
        )

        self.volume1 = Volume.objects.create(
            volume_title=self.title1,
            volume_name='1',
            volume_price=1,
            volume_number=1,
        )
        self.volume2 = Volume.objects.create(
            volume_title=self.title1,
            volume_name='2',
            volume_price=2,
            volume_number=2,
        )

        self.chapter_1_1 = Chapter.objects.create(
            volume=self.volume1,
            chapter_number=1,
            chapter_content='123'
        )
        self.chapter_1_2 = Chapter.objects.create(
            volume=self.volume1,
            chapter_number=2,
            chapter_content='123'
        )
        self.chapter_2_1 = Chapter.objects.create(
            volume=self.volume2,
            chapter_number=1,
            chapter_content='123'
        )

        self.title2.tags.add(self.tag1)
        self.title2.tags.add(self.tag2)


class APIUrlsTests(TestCase, DBTestItemsDefault):

    def setUp(self) -> None:
        self.create_test_db_items()

    def test_get_titles_is_resolved(self):
        url = reverse('title_view')
        self.assertEqual(resolve(url).func.view_class, TitleView)

    def test_get_single_title_is_resolved(self):
        url = reverse('single_title_view', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, SingeTitleView)

    def test_get_chapters_is_resolved(self):
        url = reverse('chapter_view')
        self.assertEqual(resolve(url).func.view_class, ChapterView)

    def test_get_single_chapter_is_resolved(self):
        url = reverse('single_chapter_view', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, SingleChapterView)

    def test_get_titles_is_responding(self):
        url = f'{base_endpoint}/titles/'
        response = client.get(url)
        self.assertEqual(200, response.status_code)

    def test_get_single_title_is_responding(self):
        url = f'{base_endpoint}/titles/1/'
        response = client.get(url)
        self.assertEqual(200, response.status_code)

    def test_get_chapters_is_responding(self):
        url = f'{base_endpoint}/chapters/'
        response = client.get(url)
        self.assertEqual(200, response.status_code)

    def test_get_single_chapter_is_responding(self):
        url = f'{base_endpoint}/chapters/1/'
        response = client.get(url)
        self.assertEqual(200, response.status_code)


class TitlesAPIViewTests(TestCase, DBTestItemsDefault):
    def setUp(self) -> None:
        self.create_test_db_items()

    def test_all_titles_pagination(self):
        response = client.get(f'{base_endpoint}/titles/?page=1&per_page=1')
        obj = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(obj['results']))

    def test_all_titles_pagination_error(self):
        response = client.get(f'{base_endpoint}/titles/?page=-10&per_page=1')
        obj = response.json()

        self.assertEqual(404, response.status_code)
        self.assertEqual("Invalid page.", obj['detail'])

    def test_all_titles_query(self):
        response = client.get(f'{base_endpoint}/titles/')
        obj = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, obj['count'])
        self.assertEqual(2, len(obj['results'][1]['tags']))
        self.assertFalse(obj['results'][1]['description'])

    def test_single_title_query(self):
        response = client.get(f'{base_endpoint}/titles/1/')
        obj = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(obj['volume_titles']))
        self.assertEqual(2, len(obj['volume_titles'][1]['volume_chapters']))
        self.assertEqual(1, len(obj['volume_titles'][0]['volume_chapters']))

    def test_single_title_query_error(self):
        response = client.get(f'{base_endpoint}/titles/0/')
        obj = response.json()

        self.assertEqual(404, response.status_code)
        self.assertEqual("Not found.", obj['detail'])


class ChaptersAPIViewTests(TestCase, DBTestItemsDefault):
    def setUp(self) -> None:
        self.create_test_db_items()

    def test_all_chapters_pagination(self):
        response = client.get(f'{base_endpoint}/chapters/?page=1&per_page=1')
        obj = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(obj['results']))

    def test_all_chapters_pagination_error(self):
        response = client.get(f'{base_endpoint}/chapters/?page=-10&per_page=1')
        obj = response.json()

        self.assertEqual(404, response.status_code)
        self.assertEqual("Invalid page.", obj['detail'])

    def test_all_chapters_query(self):
        response = client.get(f'{base_endpoint}/chapters/')
        obj = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(3, obj['count'])

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_single_chapter_query(self):
        response = client.get(f'{base_endpoint}/chapters/1/')
        obj = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, obj['data']['chapter_views_count'])

        for i in range(4):
            increase_view.delay(1)
        time.sleep(3)

        response2 = client.get(f'{base_endpoint}/chapters/1/')
        obj2 = response2.json()

        self.assertEqual(200, response2.status_code)
        self.assertEqual(5, obj2['data']['chapter_views_count'])

    def test_single_chapter_query_error(self):
        response = client.get(f'{base_endpoint}/chapters/0/')
        obj = response.json()

        self.assertEqual(404, response.status_code)
        self.assertEqual("Chapter not exists", obj['message'])

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_post_like_chapter(self):
        response = client.get(f'{base_endpoint}/chapters/2/')
        obj = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, obj['data']['chapter_views_count'])
        self.assertEqual(0, obj['data']['chapter_likes_count'])

        for i in range(5):
            increase_like.delay(2)
        time.sleep(3)

        response2 = client.get(f'{base_endpoint}/chapters/2/')
        obj2 = response2.json()
        self.assertEqual(200, response2.status_code)
        self.assertEqual(5, obj2['data']['chapter_likes_count'])
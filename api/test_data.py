import string
import random

from api.models import Title, Volume, Chapter, Tags


def create_random_titles(count):
    for _ in range(int(count)):
        Title.objects.create(
            ru_name=''.join(random.sample(string.ascii_letters, 20)),
            en_name=''.join(random.sample(string.ascii_letters, 20)),
            alt_name=''.join(random.sample(string.ascii_letters, 20)) if random.randint(0, 1) else None,
            description=''.join(random.sample(string.ascii_letters, 20)) if random.randint(0, 1) else ''
        )


def create_random_tags(count):
    for _ in range(int(count)):
        Tags.objects.create(
            tag_name=''.join(random.sample(string.ascii_letters, 30))
        )


def create_test_items():
    vipe_database()
    tag1 = Tags.objects.create(
        tag_name='Тег 1'
    )
    tag2 = Tags.objects.create(
        tag_name='Тег 2'
    )
    tag3 = Tags.objects.create(
        tag_name='Тег 3'
    )
    title1 = Title.objects.create(
        ru_name='Тайтл 1',
        en_name='Title 1',
        alt_name='title_1',
        description='Это 1ый тайтл'
    )
    title1.tags.add(tag1)
    title1.tags.add(tag3)
    title2 = Title.objects.create(
        ru_name='Тайтл 2',
        en_name='Title 2',
        alt_name='title_2',
        description='Это 2ый тайтл'
    )
    title2.tags.add(tag2, tag3)
    title3 = Title.objects.create(
        ru_name='Тайтл 3',
        en_name='Title 3',
    )
    create_random_titles(50)
    create_random_tags(5)
    volume1 = Volume.objects.create(
        volume_title=title1,
        volume_name='1ый Вол тайтла 1',
        volume_price=10,
        volume_number=1,
    )

    volume2 = Volume.objects.create(
        volume_title=title1,
        volume_name='2ой Вол тайтла 1',
        volume_price=20,
        volume_number=2,
    )

    volume3 = Volume.objects.create(
        volume_title=title2,
        volume_name='1ый Вол тайтла 1',
        volume_price=999,
        volume_number=1,
    )

    chapter1 = Chapter.objects.create(
        volume=volume1,
        chapter_number=1,
        chapter_content='cont 1',
    )
    chapter2 = Chapter.objects.create(
        volume=volume1,
        chapter_number=2,
        chapter_content='cont 2',
    )

    chapter3 = Chapter.objects.create(
        volume=volume3,
        chapter_number=1,
        chapter_content='cont 1',
    )


def vipe_database():
    for queryset in [Tags.objects.all(), Chapter.objects.all(), Volume.objects.all(), Title.objects.all()]:
        for item in queryset:
            try:
                item.delete()
            except:
                continue
    assert all([len(i) == 0 for i in [Tags.objects.all(), Chapter.objects.all(),
                                      Volume.objects.all(), Title.objects.all()]])

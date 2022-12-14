import sqlite3

import django.db.utils
from celery import shared_task
from django.db.models import F

from .models import Chapter


@shared_task(autoretry_for=(django.db.utils.OperationalError, sqlite3.OperationalError),
             retry_backoff=True,
             retry_kwargs={'max_retries': 25},
             retry_backoff_max=1)
def increase_view(pk):
    Chapter.objects.filter(id=pk).update(chapter_views_count=F('chapter_views_count') + 1)


@shared_task(autoretry_for=(django.db.utils.OperationalError, sqlite3.OperationalError),
             retry_backoff=True,
             retry_kwargs={'max_retries': 25},
             retry_backoff_max=1)
def increase_like(pk):
    Chapter.objects.filter(id=pk).update(chapter_likes_count=F('chapter_likes_count') + 1)
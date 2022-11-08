import sqlite3

import django.db.utils
from django.db import transaction
from celery import shared_task

from .models import Chapter


@shared_task(autoretry_for=(django.db.utils.OperationalError, sqlite3.OperationalError),
             retry_backoff=True,
             retry_kwargs={'max_retries': 25},
             retry_backoff_max=1)
@transaction.atomic
def increase_view(pk):
    model = Chapter.objects.get(pk=pk)
    model.chapter_views_count += 1
    model.save()


@shared_task(autoretry_for=(django.db.utils.OperationalError, sqlite3.OperationalError),
             retry_backoff=True,
             retry_kwargs={'max_retries': 25},
             retry_backoff_max=1)
@transaction.atomic
def increase_like(pk):
    model = Chapter.objects.get(pk=pk)
    model.chapter_likes_count += 1
    model.save()
from __future__ import absolute_import

import os

from celery import Celery

from celery import shared_task


@shared_task
def add(x, y):
    return x + y

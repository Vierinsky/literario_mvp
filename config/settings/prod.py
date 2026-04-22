import os

from .base import *

DEBUG = False

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

CSEF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
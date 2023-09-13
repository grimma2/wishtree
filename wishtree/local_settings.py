from pathlib import Path


DEBUG = True

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '*t^&ry&^uyfGy(^iytGVT7I6f&iuyUG6RF7^%$%)'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ALLOWED_HOSTS = []

EMAIL_HOST_USER = 'andrey.chella@mail.ru'
EMAIL_HOST_PASSWORD = 'KVFfxjLcp0Vk2EJ98Mf3'

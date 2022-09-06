from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

#SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'zizi',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '',
    }
}

#server
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'zizi',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '',
    }
}

#Ubuntu
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'zizi_projeto',
        'USER': 'zizi_user',
        'PASSWORD': 'zizi2121',
        'HOST': '192.168.100.76',
        'PORT': '5432',
    }
}

DEBUG = True

# heroku deploy

# heroku list
# git remote -v
# git status
# git add .
# git status
# git commit -m "alteraçao nova"
# git remote -v
# git push heroku master
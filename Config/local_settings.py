from .common import *

DATABASES = {'default': dj_database_url.parse(os.environ['DATABASE_URL'])}
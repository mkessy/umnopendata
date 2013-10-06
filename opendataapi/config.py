##### START APP CONFIG

CSRF_ENABLED = True
SECRET_KEY = 'dev-key'

from os.path import abspath, dirname, join
BASE_DIR = abspath(dirname(__file__))

##### DATABASE CONFIG
SQLALCHEMY_DATABASE_URI = 'postgresql://dev_local:devpw@localhost/opendata_dev'

##### END DATABASE CONFIG

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os

BASE_DIR = settings.BASE_DIR

ENV_PAT = """
DEBUG={}
SECRET_KEY={}
ALLOWED_HOSTS=
INSTALLED_APPS=

LANGUAGE_CODE=
TIME_ZONE=

DEFAULT_FROM_EMAIL=
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=
EMAIL_PORT=
EMAIL_USE_TLS=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

STATIC_ROOT=

LOG_PATH=
LOG_LEVEL=
LOG_HANDLERS=

# DATABASE
DEFAULT_DB_ENGINE=
#DEFAULT_DB_OPTIONS=
DEFAULT_DB_NAME=
DEFAULT_DB_USER=
DEFAULT_DB_PASSWORD=
DEFAULT_DB_HOST=
DEFAULT_DB_PORT=

# MONGODB
MONGODB_USER=
MONGODB_PASSWORD=
MONGODB_HOST=
MONGODB_NAME=

# Token Manager
TOKEN_MANAGER_SECRET=
""".strip()


class Command(BaseCommand):
    help = "Creates a .env file for the project"
    file_path = os.path.join(BASE_DIR, '.env')

    def add_arguments(self, parser):
        parser.add_argument('--production', metavar='production',
                            type=bool, const=True, nargs='?',
                            help="is it production environment?")

    def write_env(self, CONFIG_STRING):
        with open(self.file_path, 'w') as f:
            f.write(CONFIG_STRING)

    def handle(self, *args, **options):
        secrete_key = os.urandom(50)
        self.stdout.write(self.style.SUCCESS('Creating .env file...'))
        debug = False if options.get('production') else True
        self.write_env(ENV_PAT.format(debug, secrete_key))
        self.stdout.write(self.style.SUCCESS('Successfully created .env'))

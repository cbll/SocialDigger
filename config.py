from os.path import abspath, dirname, join
# Absolute filesystem path to the Flask project directory:
PROJECT_ROOT = dirname(abspath(__file__))
MEDIA_ROOT = join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'very-very-secret-key'

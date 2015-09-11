from os.path import abspath, dirname, join
# Absolute filesystem path to the Flask project directory:
PROJECT_ROOT = dirname(abspath(__file__))
WC_IMAGES_ROOT = join(PROJECT_ROOT, 'app/static/wc_images')
WC_IMAGES_URL = '/static/wc_images/'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'very-very-secret-key'

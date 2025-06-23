import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-kyaqp9kt2q@&x(nbndoxf6@3&-jad$nv6*9sc&&&)95%q$)c=t'
DEBUG = True 
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'ckeditor',
    'taggit',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'blog' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog_project.wsgi.application'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'blog_project',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'blog' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' 

# CKEditor Configuration
# Settings for the rich text editor used in blog posts

CKEDITOR_UPLOAD_PATH = "uploads/"  # Directory for uploaded files via CKEditor
CKEDITOR_IMAGE_BACKEND = "pillow"  # Image processing backend

# CKEditor toolbar configurations
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # Full toolbar with all options
        'height': 300,  # Editor height in pixels
        'width': '100%',  # Editor width
        'extraPlugins': ','.join([
            'uploadimage',  # Image upload
            'autolink',  # Auto-link detection
            'autoembed',  # Auto-embed media
            'embedsemantic',  # Semantic embedding
            'autogrow',  # Auto-resize editor
            'widget',  # Widget system
            'lineutils',  # Line utilities
            'clipboard',  # Clipboard operations
            'dialog',  # Dialog system
            'dialogui',  # Dialog UI
            'elementspath'  # Element path
        ]),
    },
    'blog': {
        'toolbar': [
            ['Bold', 'Italic', 'Underline', 'Strike'],  # Text formatting
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],  # Lists and indentation
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],  # Text alignment
            ['Link', 'Unlink'],  # Link management
            ['Image', 'Table', 'HorizontalRule'],  # Media and tables
            ['Format', 'Font', 'FontSize'],  # Text formatting options
            ['TextColor', 'BGColor'],  # Color options
            ['Source']  # HTML source view
        ],
        'height': 400,  # Editor height for blog posts
        'width': '100%',  # Full width
    }
}


#EMAIL SETTINGS
# Configuration for sending emails (used by contact form)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # SMTP backend
EMAIL_HOST = 'smtp.gmail.com'  # Gmail SMTP server
EMAIL_PORT = 587  # SMTP port for TLS
EMAIL_USE_TLS = True  # Use TLS encryption
EMAIL_HOST_USER = 'talkwithharpreet@gmail.com'  # Gmail account
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Default sender email
EMAIL_HOST_PASSWORD = 'ldjqbszfodflytmf'  # Use Gmail App Password (not your Gmail password)
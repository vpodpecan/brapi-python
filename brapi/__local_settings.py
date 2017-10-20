DEBUG = False

# enter database details and credentials
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.?',
        'USER': 'django',
        'NAME': 'brapi',
        'PASSWORD': '?',
        'HOST': 'localhost',
        'PORT': ''
    }
}

# fill in your domain (or '*' but this is not recommended)
ALLOWED_HOSTS = []

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

# SECURITY WARNING: keep the secret key used in production secret!
# NOTE: this is a sample key, you should make your own for your production server!
SECRET_KEY = 'k*s8dx9x0zfn%zm^gj48xmb8d)z8-3ymo$fybpqif1ib-qld!m'

"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9-c(y)z^8040c%&h%agep0)*n+#vlv^*3^pidg4)fg6ix0hq#n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tradehub',
    'account',
    'api',
    'crispy_forms',
    'crispy_bootstrap5',
     'rest_framework',
     'rest_framework.authtoken',
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), BASE_DIR / 'tradehub/templates', BASE_DIR / 'account/templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tradehub',  # Oluşturduğunuz veritabanı adı
        'USER': 'oskay',    # Veritabanı kullanıcı adınız
        'PASSWORD': 'q1w2e3r4t5',  # Veritabanı şifreniz
        'HOST': 'localhost',   # veya uzak bir sunucu adresi
        'PORT': '5432',        # PostgreSQL'in varsayılan portu
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), BASE_DIR / 'tradehub/static', BASE_DIR / 'account/static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


USE_L10N = True
USE_THOUSAND_SEPARATOR = True


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


#todoList
#DONE: Asset Detail Page Oluşturulacak (Page Design + View)
    #DONE: Grafik ekleme işlevini de chart.js kullanarak gerçekleştir. Notionda nasıl yapalacağı task içinde anlatıldı.
        #DONE: Grafiği mobil uyumlu hale getir CSS
    #DONE: Add Asset Transcation Page'i Formu ile beraber oluştur.
    #DONE: Asset Detail Page'e .'lardan cost'ları ayırmaya yönelik filter oluşturulacak -> örn 1000000 to 1.000.000.00
#DONE:Asset Transcation LOG Delete Functionality
    #DONE: Update Stats after deleting the logs (Direkt JS ile sayfanın yeniden yüklenmesi sağlanabilir. JS ile backende istek atıp güncel dataları alma ile uğraşmak ekstra efor olabilir.)
#DONE:Asset Log Detail Sayfasında, dashboard da logları sıralarken tersten yani en son girilen işlem en üstte olacak şekilde düzenleme yapılacak.
#DONE:Asset Detail Sayfalarında Asset log sayısını 10 dan fazla arttır ve pagination yapısını kontrol et.
#DONE: Paginated Sayfalar arasında gezinmek için UI elementi oluştur.
#DONE: Buy ve Sell şeklinde iki farklı işlem yapısı oluşturulacak. Yapılan işleme göre asset dashboard update edilecek
#DONE:Asset Category sayfalarında listelenen assetlerin (kullanıcı isterse) silinmesini sağlayacak JS sistemini kur.
#DONE: Account Register, Login, Logout İşlemleri Oluşturulacak.
#DONE: Profile section on navbar and Password Change Page oluşturulacak.
#DONE: Mobile Navbar düzenlemesi yapılacak.
#DONE: Rest API Oluşturulacak
#DONE: Rest API ile Category Asset ve Category Listeleme işlemleri gerçekleştirilecek.
#DONE: Rest API ile Asset Categories, Category Assets, Asset Detail (GET) Endpoints oluşturulacak
#DONE: Rest API ile Category Asset Create (POST) ENDPOİNT oluşturulacak
#DONE: Rest API ile Asset Detail (LOG Create) (POST) ENDPOİNT oluşturulacak
#DONE: Rest API ile Asset Detail (LOG DELETE) (DELETE) ENDPOINT oluşturulacak
#DONE: Rest API Category Assets Delete Endpoint oluşturulacak
#DONE: Navbar üzerindeki Profile kısmına tıklanınca API token section açılarak kullanıcının token bilgilerini görmesi için ekstra sayfa sağlanacak. Kulalnıcı isterse ilgili sayfadan tokenını alabilecek yada yeni token talebi oluşturulabilecek.
#DONE: Readme.md içerisine kullanıcının token almasını sağlayan URl (endpoint) bilgisi eklenecek
#DONE: Her kullanıcı kayıt olduğunda otomatik o kullanıcı için token oluşturma işlemini sağlayan otomasyon kurulacak ve bu yapı ile alakalı bilgi readme.md'ye eklenecek.
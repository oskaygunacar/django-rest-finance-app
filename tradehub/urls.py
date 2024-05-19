from django.contrib import admin
from django.urls import path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'tradehub'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<slug:asset_category_slug>/add-new-asset/', views.add_new_asset, name='add_new_asset'),
    path('assets/<slug:asset_category_slug>/', views.asset_category, name='asset_category')
]
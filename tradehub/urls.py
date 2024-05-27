from django.contrib import admin
from django.urls import path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'tradehub'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    # Asset Category
    path('<slug:asset_category_slug>/add-new-asset/', views.add_new_asset, name='add_new_category_asset'), # category yeni asset ekleme
    path('assets/<slug:asset_category_slug>/', views.asset_category, name='asset_category'), # asset category detail
    # Asset
    path('asset/<slug:asset_slug>/', views.asset_logs, name='asset_logs'), #asset detail - asset transaction logs
    path('asset/add-new-transcation/<slug:asset_slug>/', views.add_new_asset_transcation, name='add_new_asset_transcation'), # yeni asset işlemi ekleme
    path('<slug:asset_slug>/delete-asset-logs/', views.delete_asset_transcation, name='delete_an_asset_transcation'), # asset loglardan bir log silme
]
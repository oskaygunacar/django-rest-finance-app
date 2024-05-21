from django.contrib import admin

from .models import Category, Asset

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['category','name', 'asset_image','amount','cost','ort_usd','user']
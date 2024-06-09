from django.contrib import admin

from .models import Category, Asset

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_display_links = ['name', 'slug']

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['id', 'category','name','slug','amount','cost','ort_usd','user']
    list_display_links = ['id', 'category','name','slug','amount','cost','ort_usd','user']
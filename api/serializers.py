from rest_framework import serializers
from tradehub.models import Asset, Category

from django.urls import reverse


class CategorySerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize the categories.
    """
    category_api_url = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['name', 'category_api_url']

    def get_category_api_url(self, instance): #instance or obj or whatever it just the name of the object
        return reverse('api:all_category_assets_listing', kwargs={'category_slug': instance.slug})


class CategoryAssetsSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize the assets in a given category.
    """
    category = serializers.SerializerMethodField()
    class Meta:
        model = Asset
        fields = ['category','name']

    def get_category(self, obj):
        return obj.category.name
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
    asset_api_detail_url = serializers.SerializerMethodField()
    asset_api_transaction_url = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = ['category','name', 'asset_api_detail_url', 'asset_api_transaction_url']

    def get_category(self, obj):
        return obj.category.name
    
    def get_asset_api_detail_url(self, instance):
        return reverse('api:asset_detail', kwargs={'category_slug': instance.category.slug,'asset_slug': instance.slug})
    
    def get_asset_api_transaction_url(self,instance):
        return reverse('api:add_asset_transaction', kwargs={'category_slug': instance.category.slug,'asset_slug': instance.slug})
    
class AssetSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize the assets.
    """
    user = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    class Meta:
        model = Asset
        fields = ['user','category', 'name', 'amount', 'cost', 'ort_usd', 'logs']

    def get_user(self, obj):
        return obj.user.username
    
    def get_category(self, obj):
        return obj.category.name
    

class AssetCreateSerializer(serializers.ModelSerializer):
    """
    This serializer is used to create a new asset in the given category
    """
    class Meta:
        model = Asset
        fields = ['name']

class AssetTransactionSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize the asset transactions.
    """
    transaction_type = serializers.CharField(required=True)

    def validate_transaction_type(self, value):
        """
        This method is used to validate the transaction type.
        """
        if value.lower() not in ['buy', 'sell']:
            raise serializers.ValidationError("The transaction type you entered is invalid. Please enter either 'Buy/buy' or 'Sell/sell'.")
        return value
    
    class Meta:
        model = Asset
        fields = ['amount', 'cost', 'transaction_type']
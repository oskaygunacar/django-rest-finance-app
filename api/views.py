from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import CategoryAssetsSerializer, CategorySerializer, AssetSerializer, AssetCreateSerializer, AssetTransactionSerializer

# models
from tradehub.models import Asset, Category
from django.contrib.auth.models import User

@api_view(http_method_names=['GET'])
def all_categories(request, *args, **kwargs):
    """
    This view returns all categories.
    """
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True,context={'request': request})
    return Response(serializer.data)
 

@api_view(http_method_names=['GET'])
def category_asset_listing_view(request, category_slug, *args, **kwargs):
    """
    This view returns all assets in a given category.
    """
    category = get_object_or_404(Category, slug=category_slug)
    user = get_object_or_404(User, id=request.user.id)
    objects = Asset.objects.filter(category=category, user=user).all()
    serializer = CategoryAssetsSerializer(objects, many=True)
    return Response(serializer.data)

@api_view(http_method_names=['GET'])
def asset_detail_view(request, category_slug, asset_slug, *args, **kwargs):
    """
    This view returns the details of a given asset.
    """
    category = get_object_or_404(Category, slug=category_slug)
    asset = get_object_or_404(Asset, slug=asset_slug, category=category, user=request.user)
    serializer = AssetSerializer(asset)
    return Response(serializer.data)

@api_view(http_method_names=['POST'])
def create_new_asset(request, category_slug, *args, **kwargs):
    """
    This view creates a new asset in the given category
    """
    category = get_object_or_404(Category, slug=category_slug)
    data = request.data
    serializer = AssetCreateSerializer(data=data)
    if serializer.is_valid():
        try:
            obj,created = Asset.objects.get_or_create(name=serializer.validated_data['name'], user=request.user, category=category)
            if not created:
                return Response({'message': 'Asset already exists', 'status': 400}, status=400)
        except:
            return Response({'message': 'An error occured while creating the asset', 'status': 500}, status=500)
        else:
            return Response({'message': 'Asset created successfully', 'status': 200}, status=200)
    return Response(serializer.errors, status=400)

@api_view(http_method_names=['POST'])
def asset_transaction_view(request, category_slug, asset_slug, *args, **kwargs):
    """
    This view is used to add a new transaction to the given asset.
    """
    category = get_object_or_404(Category, slug=category_slug)
    asset = get_object_or_404(Asset, slug=asset_slug, category=category, user=request.user)
    data = request.data
    serializer = AssetTransactionSerializer(data=data)
    if serializer.is_valid():
        try:
            # Code BUY / SELL Section
            asset.save()
        except:
            return Response({'message': 'An error occured while adding the transaction', 'status': 500}, status=500)
        else:
            return Response({'message': 'Transaction added successfully', 'status': 200}, status=200)
    return Response(serializer.errors, status=400)

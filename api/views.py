from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import CategoryAssetsSerializer, CategorySerializer

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


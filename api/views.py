from django.shortcuts import render
from django.shortcuts import get_object_or_404

from decimal import Decimal
from datetime import datetime

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
            transcation_time= datetime.now().strftime("%d/%m/%Y")
            transaction_type = serializer.validated_data['transaction_type'].lower()
            amount = serializer.validated_data.get('amount')
            cost = serializer.validated_data.get('cost', 0)
            #create decimals for amount and cost
            dec_amount = Decimal(amount)
            dec_cost = Decimal(cost)

            if transaction_type == 'sell' and amount > asset.amount:
                return Response({'message': 'You cannot sell more than you have', 'status': 400}, status=400)
            elif transaction_type == 'sell' and amount <= asset.amount:
                asset.amount -= dec_amount
                asset.cost -= dec_amount * asset.ort_usd
                if asset.amount <= 0:
                    previous_ort_usd = str(asset.ort_usd)
                asset.ort_usd = 0 if asset.amount <= 0 else asset.ort_usd
                transcation = dict(
                # id = len(asset.logs) + 1,
                id = max([log.get('id') for log in asset.logs]) + 1 if len(asset.logs) > 0 else len(asset.logs) + 1,
                transaction_type = transaction_type,
                transcation_time=transcation_time,
                total_amount=str(amount),

                total_cost=str(cost),
                ort_usd=str(cost / amount),
            )
                transcation['previous_ort_usd'] = previous_ort_usd if asset.amount <= 0 else str(asset.ort_usd)
                asset.logs.append(transcation)
                asset.save()
            else: # buy transcation codes.
                asset.amount += dec_amount
                asset.cost += dec_cost
                asset.ort_usd = asset.cost / asset.amount
                transcation = dict(
                    id = max([log.get('id') for log in asset.logs]) + 1 if len(asset.logs) > 0 else len(asset.logs) + 1,
                    transaction_type=transaction_type,
                    transcation_time=transcation_time,
                    total_amount=str(amount),
                    total_cost=str(cost),
                    ort_usd=str(cost / amount),
                )
                asset.logs.append(transcation)
                asset.save()
        except Exception as e:
            print(e)
            return Response({'message': 'An error occured while adding the transaction', 'status': 500}, status=500)
        else:
            return Response({'message': 'Transaction added successfully', 'status': 200, 'transaction':transcation}, status=200)
    return Response(serializer.errors, status=400)


# DELETE Views

@api_view(http_method_names=['DELETE'])
def remove_category_asset(request, category_slug, asset_slug):
    """
    This view is used to remove an asset from the given category.
    """
    category = get_object_or_404(Category, slug=category_slug)
    asset = get_object_or_404(Asset, slug=asset_slug, category=category, user=request.user)
    asset.delete()
    return Response({'message': f'Asset removed from the {category} category successfully', 'status': 200}, status=200)

@api_view(http_method_names=['DELETE'])
def remove_asset_transaction(request, category_slug, asset_slug, transaction_id, *args, **kwargs):
    """
    This view is used to remove a transaction from the given asset.
    """
    category = get_object_or_404(Category, slug=category_slug)
    asset = get_object_or_404(Asset, slug=asset_slug, category=category, user=request.user)
    try:
        for log in asset.logs:
            if log.get('id') == transaction_id:
                if log.get('transaction_type') == 'sell':
                    asset.amount += Decimal(log.get('total_amount'))
                    asset.cost += Decimal(log.get('total_cost'))
                    asset.ort_usd = asset.cost / asset.amount
                elif log.get('transaction_type') == 'buy' and asset.amount - Decimal(log.get('total_amount')) < 0:
                    return Response({'message': 'Asset Amount cant be "-"', 'status': 400}, status=400)
                else:
                    asset.amount -= Decimal(log.get('total_amount'))
                    asset.cost -= Decimal(log.get('total_cost'))
                    asset.ort_usd = Decimal(asset.cost / asset.amount) if asset.amount != 0 else 0
                asset.logs.remove(log)
                asset.save()
                return Response({'message': 'Transaction removed successfully', 'status': 200, 'transaction':log}, status=200)
    except:
        return Response({'message': 'An error occured while removing the transaction', 'status': 500}, status=500)
    return Response({'message': 'Transaction not found', 'status': 404}, status=404) # 
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator

#models
from .models import Asset, Category

#modelForms
from .forms import AssetForm, AssetTranscationForm

#python
from datetime import datetime

def homepage(request):
    return render(request, 'tradehub/homepage.html', context={})

def asset_category(request, asset_category_slug):
    """
    Lists all the assets that user have in the given "asset" category
    """
    user = request.user
    category = get_object_or_404(Category, slug=asset_category_slug)
    assets = Asset.objects.filter(user=user, category=category)
    context = dict(assets=assets, title=category.name, category=category)
    return render(request, 'tradehub/assetListing.html', context=context)


def add_new_asset(request, asset_category_slug):
    """
        Adds a new asset to the given "asset" category
    """
    form = AssetForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.name = form.cleaned_data.get('name').title()
        obj.user = request.user
        category = get_object_or_404(Category,slug=asset_category_slug)
        obj.category = category
        saved_obj = obj.save()
        # return redirect('tradehub:asset', slug=saved_obj.slug) # BURAYI DÜZENLE !!!!
        return redirect('tradehub:homepage') # geçici redirect
    context = dict(form=form, category=asset_category_slug.title())
    return render(request, 'tradehub/addNewAsset.html', context=context)


def asset_logs(request, asset_slug):
    asset = get_object_or_404(Asset, slug=asset_slug, user=request.user)
    all_logs = asset.logs # all asset transcation logs
    paginator = Paginator(all_logs, 10)
    page_number = request.GET.get('page')
    if page_number == 1:
        return redirect('tradehub:asset_logs', asset_slug=asset_slug)
    logs = paginator.get_page(page_number)
    context = dict(asset=asset, logs=logs)
    return render(request, 'tradehub/asset.html', context=context)

def add_new_asset_transcation(request, asset_slug):
    """
    Adds a new transcation to the given "asset"
    """
    form = AssetTranscationForm(request.POST or None)
    asset = get_object_or_404(Asset, slug=asset_slug, user=request.user)
    if form.is_valid():
        transcation = dict(
            transcation_time= datetime.now().strftime("%d/%m/%Y"),
            total_amount=form.cleaned_data.get('amount'),
            avg_price_try=form.cleaned_data.get('avg_price_try'),
            avg_usd=form.cleaned_data.get('avg_usd'),
        )
        asset.logs.append(transcation)
        asset.save()
        return redirect('tradehub:asset_logs', asset_slug=asset_slug)
    context = dict(form=form, asset=asset)
    return render(request, 'tradehub/addNewAssetTranscation.html', context=context)
    

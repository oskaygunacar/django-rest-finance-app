from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator

#models
from .models import Asset, Category

#modelForms
from .forms import AssetForm, AssetTranscationForm

#python
from datetime import datetime
from decimal import Decimal
import json

def homepage(request):
    return render(request, 'tradehub/homepage.html', context={})

def asset_category(request, asset_category_slug):
    """
    Lists all the assets that user have in the given "asset" category
    """
    user = request.user
    category = get_object_or_404(Category, slug=asset_category_slug)
    assets = Asset.objects.filter(user=user, category=category)
    context = dict(assets=assets, title=category.name)
    return render(request, 'tradehub/assetListing.html', context=context)


def add_new_asset(request, asset_category_slug):
    """
        Adds a new asset to the given "asset" category
    """
    form = AssetForm(request.POST or None, request.FILES or None)
    category = get_object_or_404(Category,slug=asset_category_slug) # if there is no category, it will raise 404
    if form.is_valid():
        obj = form.save(commit=False)
        obj.name = form.cleaned_data.get('name').title()
        obj.user = request.user
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
    data = [cost['ort_usd'] for cost in logs]
    labels = [index +1 for index, label in enumerate(data)]
    context = dict(asset=asset, logs=logs, category=asset.category.name, data=data, labels=labels)
    return render(request, 'tradehub/asset.html', context=context)

def rounder(sayi, basamak):
    carpani = 10 ** basamak
    return round(sayi * carpani) / carpani

def add_new_asset_transcation(request, asset_slug):
    """
    Adds a new transcation to the given "asset"
    """
    form = AssetTranscationForm(request.POST or None)
    asset = get_object_or_404(Asset, slug=asset_slug, user=request.user)
    if form.is_valid():
        transcation_time= datetime.now().strftime("%d/%m/%Y")
        total_amount=form.cleaned_data.get('total_amount')
        total_cost = form.cleaned_data.get('total_cost')

        # Decimal dönüştürme
        dec_total_amount = Decimal(total_amount)
        dec_total_cost = Decimal(total_cost)

        asset.amount += dec_total_amount
        asset.cost += dec_total_cost
        asset.ort_usd = asset.cost / asset.amount
        asset.save()
        transcation = dict(
            id = len(asset.logs) + 1,
            transcation_time=transcation_time,
            total_amount=total_amount,
            total_cost=total_cost,
            ort_usd=str(total_cost / total_amount),
        )
        asset.logs.append(transcation)
        asset.save()
        return redirect('tradehub:asset_logs', asset_slug=asset_slug)
    context = dict(form=form, asset=asset, category=asset.category.name)
    return render(request, 'tradehub/addNewAssetTranscation.html', context=context)
    

def delete_asset_transcation(request, asset_slug):
    if request.method == "POST":
        asset = get_object_or_404(Asset, slug=asset_slug, user=request.user)
        items_to_delete = json.loads(request.body)
        print(items_to_delete)
        for item in items_to_delete: # items_to_delete includes ids that selected by user before clicked on delete logs button
            print(item, type(item))
            for index, log in enumerate(asset.logs):
                if int(log.get('id')) == int(item):
                    # print(log, type(log))
                    asset.amount -= Decimal(log.get('total_amount'))
                    asset.cost -= Decimal(log.get('total_cost'))
                    asset.ort_usd = asset.cost / asset.amount if asset.amount != 0 else 0
                    asset.logs.pop(index)
        asset.save()
        return redirect('tradehub:asset_logs', asset_slug=asset_slug)

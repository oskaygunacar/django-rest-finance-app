from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404

#models
from .models import Asset, Category

#modelForms
from .forms import AssetForm

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

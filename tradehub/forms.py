from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'asset_image']

class AssetTranscationForm(forms.Form):
    total_amount = forms.FloatField()
    avg_price_try = forms.FloatField()
    avg_usd = forms.FloatField()
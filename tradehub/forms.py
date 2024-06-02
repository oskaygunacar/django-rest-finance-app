from django import forms
from .models import Asset
from django.core.exceptions import ValidationError

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'asset_image']

def validate_non_negative(value):
    if value < 0:
        raise ValidationError('Value cannot be negative')
    
def validate_asset_amount (value):
    if value < 0 or value == 0:
        raise ValidationError('Asset amount cannot be 0 or negative')

class AssetTranscationForm(forms.Form):
    total_amount = forms.FloatField(label='Total Asset Amount', validators=[validate_non_negative, validate_asset_amount])
    total_cost = forms.FloatField(label='Total Cost ($)', validators=[validate_non_negative])
    transaction_type = forms.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell')], label='Transaction Type')
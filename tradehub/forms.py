from django import forms
from .models import Asset
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, ROUND_DOWN

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'asset_image']

def validate_non_negative(value):
    if value < 0:
        raise ValidationError('Value cannot be negative')
    
def validate_asset_amount (value):
    if value <= 0:
        raise ValidationError('Asset amount cannot be 0 or negative')
    
def validate_max_length(value):
    if len(str(value).replace('.', '').replace('-', '')) > 18:
        raise ValidationError('Value is too big, it should not be longer than 18 digits')

class AssetTranscationForm(forms.Form):
    total_amount = forms.DecimalField(label='Total Asset Amount', max_digits=28, decimal_places=10, validators=[validate_asset_amount, validate_max_length])
    total_cost = forms.DecimalField(label='Total Cost ($)', max_digits=26, decimal_places=2, validators=[validate_non_negative, validate_max_length])
    transaction_type = forms.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell')], label='Transaction Type')
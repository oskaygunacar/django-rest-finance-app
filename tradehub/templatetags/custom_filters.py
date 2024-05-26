from django import template
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

register = template.Library()

@register.filter
def format_decimal(value):
    try:
        # Decimal türüne dönüştür
        value = Decimal(value)
        # Gereksiz sıfırları kaldır ve noktadan sonraki basamakları kontrol et
        formatted_value = value.quantize(Decimal('1.0000000000'), rounding=ROUND_HALF_UP).normalize()
        return formatted_value
    except (ValueError, TypeError, InvalidOperation):
        return value

@register.filter
def format_cost(value):
    try:
        # Decimal türüne dönüştür
        value = Decimal(value)
        # Sayıyı string olarak formatla ve gerekli yerlerde nokta ekle
        value_str = "{:,.2f}".format(value)
        value_str = value_str.replace(",", ".")
        return value_str
    except (ValueError, TypeError, InvalidOperation):
        return value
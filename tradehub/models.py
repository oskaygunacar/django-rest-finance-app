from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# python
import string, random
from decimal import Decimal, ROUND_HALF_UP

# 3rd party
from autoslug import AutoSlugField


class Category(models.Model):
    name = models.CharField(max_length=1000)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('tradehub:asset_category', kwargs={'asset_category_slug': self.slug})


class Asset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='generate_random_slug', unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=50, decimal_places=10, default=0)
    cost = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    ort_usd = models.DecimalField(max_digits=100, decimal_places=10, default=0)
    logs = models.JSONField(null=True, blank=True, default=list)
    asset_image = models.ImageField(upload_to='asset/', blank=True, null=True)

    def save(self, *args, **kwargs):
        def round_decimal(value, decimal_places):
            """Belirtilen ondalık hassasiyete göre yuvarlar, yalnızca gerekli olduğunda"""
            if value is not None:
                # Str'e çevirip ondalık noktadan sonrasına bak
                str_value = str(value)
                if '.' in str_value: # str'ye çevrilen değerde ondalık nokta var mı diye kontrol ediyoruz.
                    integer_part, fractional_part = str_value.split('.') # Eğer varsa devamında tuple ataması ile integer ve fractional partları ayırıyoruz.
                    if len(fractional_part) > decimal_places:
                        rounding_precision = Decimal('1.' + '0' * decimal_places)
                        value = value.quantize(rounding_precision, rounding=ROUND_HALF_UP)
            return value

        self.amount = round_decimal(self.amount, 10)
        self.cost = round_decimal(self.cost, 3)
        self.ort_usd = round_decimal(self.ort_usd, 10)

        super(Asset, self).save(*args, **kwargs)


    def generate_random_slug(self):
        letters = string.ascii_lowercase  # Yalnızca küçük harfler kullanılıyor
        return(''.join(random.choice(letters) for i in range(15)))
    
        # def __str__(self):
    #     return f'{self.user} - {self.amount}'

    def get_absolute_url(self):
        return reverse('tradehub:asset_logs', kwargs={'asset_slug': self.slug})



    # COİN JSON -> {'İşlem: (buy or sell)','COİN Adeti:', 'TOTAL PARA:', 'KUR:', 'USD KARŞILIĞI:'}
    # HİSSE JSON -> {'İşlem: (buy or sell)','LOT Adeti:', 'TOTAL PARA:', 'KUR':,  'USD KARŞILIĞI:'}

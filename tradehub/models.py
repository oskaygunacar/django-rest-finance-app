from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# python
import string, random

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
    name = models.CharField(max_length=1000)
    amount = models.FloatField(default=0)
    cost = models.FloatField(default=0)
    ort_usd = models.FloatField(default=0)
    logs = models.JSONField(null=True, blank=True, default=list)
    asset_image = models.ImageField(upload_to='asset/', blank=True, null=True)


    def generate_random_slug(self):
        letters = string.ascii_lowercase  # Yalnızca küçük harfler kullanılıyor
        return(''.join(random.choice(letters) for i in range(15)))
    
        # def __str__(self):
    #     return f'{self.user} - {self.amount}'

    def get_absolute_url(self):
        return reverse('tradehub:asset_logs', kwargs={'asset_slug': self.slug})



    # COİN JSON -> {'İşlem: (buy or sell)','COİN Adeti:', 'TOTAL PARA:', 'KUR:', 'USD KARŞILIĞI:'}
    # HİSSE JSON -> {'İşlem: (buy or sell)','LOT Adeti:', 'TOTAL PARA:', 'KUR':,  'USD KARŞILIĞI:'}

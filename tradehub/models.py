from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='category', blank=True, null=True)

    def __str__(self):
        return self.name
    
    # def get_absolute_url(self):
    #     return reverse('tradehub:category', kwargs={'pk': self.pk})


class Asset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=1000)
    amount = models.FloatField(default=0)
    ort_try = models.FloatField(default=0)
    ort_usd = models.FloatField(default=0)
    logs = models.JSONField(null=True, blank=True, default=list)
    asset_image = models.ImageField(upload_to='asset', blank=True, null=True)

    # def __str__(self):
    #     return f'{self.user} - {self.amount}'


    # COİN JSON -> {'İşlem: (buy or sell)','COİN Adeti:', 'TOTAL PARA:', 'KUR:', 'USD KARŞILIĞI:'}
    # HİSSE JSON -> {'İşlem: (buy or sell)','LOT Adeti:', 'TOTAL PARA:', 'KUR':,  'USD KARŞILIĞI:'}

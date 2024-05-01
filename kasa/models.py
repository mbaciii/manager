from django.db import models

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
# Create your models here.
from django.db import models
import datetime


class Product(models.Model):
    name = models.CharField(max_length=100)
    # Add any other necessary fields for the product

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Produkti')
        verbose_name_plural = _('Produktet')


class Sale(models.Model):
    store = models.CharField(max_length=2, default='d1')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_code = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=datetime.datetime.now)


    def __str__(self):
        return f"{self.product.name} - {self.price}"

    class Meta:
        verbose_name = _('Shitja')
        verbose_name_plural = _('Shitjet')





from django.contrib import admin
from django.contrib import admin
from kasa.models import Product, Sale
from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig
admin.site.index_title = _('Serenata Accessories')
admin.site.site_header = _('Menaxhuesi')
admin.site.site_title = _('Menaxhuesi')



admin.site.register(Product)
admin.site.register(Sale)
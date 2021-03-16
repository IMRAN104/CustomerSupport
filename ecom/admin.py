from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(eComCategory)
admin.site.register(eComItem)
admin.site.register(HomeItem)
admin.site.register(HomeGroup)
admin.site.register(eComItemImage)
admin.site.register(eComItemMeta)
admin.site.register(Offer)
admin.site.register(Brand)
admin.site.register(Ticker)
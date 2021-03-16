from django.db import models
from django.utils import timezone
from datetime import datetime, date
#from Xpos.models import Item as productItem
import random
import string

class Brand(models.Model):
	name = models.CharField(max_length=20,null=True)
	category = models.ManyToManyField(eComCategory)

	def __str__(self):
		return self.name

class eComItem(models.Model):
	
	item = models.OneToOneField(productItem, on_delete=models.SET_NULL, null=True)
	display_name = models.CharField(max_length=200,null=True)
	category = models.ForeignKey(eComCategory, on_delete=models.SET_NULL, null=True)
	thumbnail = models.ImageField(null=True, blank=True, upload_to='item_card_image/')
	base_price = models.DecimalField(max_digits=15,decimal_places=2, default=0)
	offer_price = models.DecimalField(max_digits=15,decimal_places=2, default=0)
	offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)
	offer_start_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
	offer_end_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
	offer_stock = models.IntegerField(default=0)
	is_archived = models.BooleanField(default=False)

	def __str__(self):
		return self.display_name
		#return self.id
	class Meta:
		ordering = ['id']


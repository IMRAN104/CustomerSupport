from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import datetime, date
#from Xpos.models import Item as productItem

class Complain(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	description = models.TextField(max_length=2000, null=False)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
	date = models.DateTimeField(null=False, auto_created=True, auto_now_add=True)
	attachment = models.FileField(null=True, blank=True, upload_to='item_card_image/')
	is_archived = models.BooleanField(default=False)
	def __str__(self):
		try:
			return "Complain:  " + str(self.user) + ": " + str(self.date) + ": " + str(self.description).split(20)
		except:
			return "Complain:  " + str(self.user) + str(self.description)
	class Meta:
		ordering = ['id']	
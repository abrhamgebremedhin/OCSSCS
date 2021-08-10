from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import User
# Create your models here.

class OCSSC_branch_office(models.Model): 
	name = models.CharField(max_length=20,blank=True)
	city = models.CharField(max_length=20,blank=True)
	address = models.CharField(max_length=20,blank=True)
	head_office = models.BooleanField(default=False)
	address = models.CharField(max_length=20,blank=True)
	#manager = models.CharField(max_length=20,blank=True)
	manager = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	created_by = models.BooleanField(default=True)
	#created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='branch_created_by')
	
	def __str__(self):
		return self.name

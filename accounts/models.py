from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractUser)
from django.contrib.auth.models import User, Permission, Group

from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from django.utils import timezone

from rest_framework.authtoken.models import Token 
from branchs.models import OCSSC_branch_office
# Create your models here.

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance) 

class User(AbstractUser):
	phone_number = models.CharField(max_length=20,blank=True)
	photograph = models.ImageField(upload_to = "user/photograph",null=True)
	identification = models.ImageField(upload_to = "user/Identification",null=True)
	address = models.CharField(max_length=100,default="")
	city = models.CharField(max_length=100,default="")
	position = models.CharField(max_length=100,default="")
	qualification_document = models.ImageField(upload_to = "user/Qualification",null=True)
	#office_branch = models.CharField(max_length=100,null=False)
	office_branch = models.ForeignKey(OCSSC_branch_office ,on_delete=models.CASCADE,null=True)
	is_manager = models.BooleanField(default=False)
	is_auditor = models.BooleanField(default=False)
	is_customer_service = models.BooleanField(default=False)
	is_system_admin = models.BooleanField(default=False)
	active = models.BooleanField(default=False) 
	date_of_hire = models.DateTimeField(null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	# created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='Employee_created_by')
class SavingType(models.Model):
	name = models.CharField(max_length=100,default="")
	detail = models.CharField(max_length=2000, default="")
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class Customer(models.Model):
	first_name = models.CharField(max_length=100,default="")
	middle_name  = models.CharField(max_length=100,default="")
	last_name  = models.CharField(max_length=100,default="")
	office_branch = models.ForeignKey(OCSSC_branch_office,on_delete=models.CASCADE,default="1")
	account_number = models.CharField(max_length=100,default="")
	phone_number = models.CharField(max_length=100,default="")
	document = models.ImageField(upload_to = "Customer/documents",null=True)
	photograph = models.ImageField(upload_to = "Customer/Identification",null=False) 
	identification = models.ImageField(upload_to = "Customer/Identification",null=True)
	address = models.CharField(max_length=100,default="")
	city = models.CharField(max_length=100,default="")
	#office_branch = models.CharField(max_length=100,default="")
	savings_type = models.ForeignKey(SavingType,on_delete=models.CASCADE)
	active = models.BooleanField(default=False) 
	initial_deposit = models.FloatField(null=False,default=0)
	date = models.DateTimeField(auto_now_add=True)
	#created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='Eustomer_created_by')

	def __str__(self):
		name = self.first_name+" "+self.middle_name+" "+self.last_name
		return name
		
class BankingHistory(models.Model):
	customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
	initial_value = models.FloatField(verbose_name=" ", max_length = 11, default=0)
	amount = models.FloatField(verbose_name=" ", max_length = 11, default=0)
	final_value = models.FloatField(verbose_name=" ", max_length = 6, default=0) 
	transaction = models.CharField(max_length=100)
	date = models.DateTimeField(auto_now_add=True) 
	#transation_handler = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='Transacted_by')




'''

OCSSC head office 

OCSSC branch office 
	name
	city
	address
	head_office
	manager
	date
	created_by 




lone processing
	status
		pending
		rejected by manager
		rejected by customer
		approved
	Loan Application Document
	contact information
	financial info
	personal id
	Financial aid required (amount)
	income statement

lone documents
	date = models.DateTimeField()
	document = 
	lone process = 





savings account
	user
	initial deposit
	account number

'''
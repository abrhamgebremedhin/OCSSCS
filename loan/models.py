from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import User,Customer
# Create your models here.
class Loan_type(models.Model):
	name = models.CharField(max_length=1000,blank=True)
	detail = models.CharField(max_length=1000,blank=True)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class Loan_processing(models.Model):
	status = models.CharField(max_length=1000,blank=True) ## pending, approved by auditor,approved by manager,granted
	customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
	loan_type = models.ForeignKey(Loan_type,on_delete=models.CASCADE)
	current_financial_info = models.ImageField(upload_to = "Loan/current_financial_info",null=True)
	business_plane = models.ImageField(upload_to = "Loan/business_plane",null=True)
	Financial_aid_required = models.FloatField(null=False,default=0)
	rejected_by_manager = models.BooleanField(default=False)
	rejected_by_customer = models.BooleanField(default=False)
	approved_by_Auditor = models.BooleanField(default=False)
	approved_by_Manager = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)
	create_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='Loan_created_by')
	manager_approved = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='Loan_Manager_approved',null=True)
	auditor_approved = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='Loan_Auditor_approved',null=True)

	def document(self):
		return self.documents_set.all()

class Documents(models.Model):
	loan = models.ForeignKey(Loan_processing,on_delete=models.CASCADE)
	image = models.ImageField(upload_to = "Loan/documents/",null=True)
	date = models.DateTimeField(auto_now_add=True)

class Conditions(models.Model):
	loan = models.ForeignKey(Loan_processing,on_delete=models.CASCADE)
	time_interval = models.CharField(max_length=1000,blank=True)
	payble_amount = models.CharField(max_length=1000,blank=True)
	time_limit = models.CharField(max_length=1000,blank=True)
	rate = models.FloatField(null=False,default=0)
	aggrement  = models.ImageField(upload_to = "Loan/aggrement",null=True) #condition_the_colateral will_be_desolved
	date = models.DateTimeField(auto_now_add=True)



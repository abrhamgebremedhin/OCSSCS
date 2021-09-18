from django.shortcuts import render,get_object_or_404
from django.views import View 
import datetime
from time import time

from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from branchs.models import OCSSC_branch_office
from .models import User,Customer,SavingType,BankingHistory,AccountNumber
from loan.models import Loan_processing
from .forms import (FrontLoginForm,UserCreationForm,AbstractUserCreationForm,
				UserCreationUpdateForm,CustomerForm,CustomerEditForm,SavingsTypeForm
				,TransactForm)

# Login view for the front end/customer user
class LoginView(auth_views.LoginView):
    form_class = FrontLoginForm
    template_name = 'registration/login.html'


class Transact(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		customer = Customer.objects.get(id=self.kwargs['id'])
		form= TransactForm()
		context = {"form":form,"customer":customer}
		template_name = "Transact/transact.html"
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = TransactForm(self.request.POST)
		customer = Customer.objects.get(id=self.kwargs['id'])
		template_name = "Transact/transact.html"
		if form.is_valid():
			if(form.cleaned_data.get('transaction') == "Deposit"):
				final_value = float(customer.initial_deposit)+float(form.cleaned_data.get('amount'))
				print(final_value)
				print("Deposited") 
			if(form.cleaned_data.get('transaction') == "Withdrow"):
				final_value = float(customer.initial_deposit)-float(form.cleaned_data.get('amount'))
				print(final_value)
				print("Withdraw")
			transact =BankingHistory( customer = customer,
					 	initial_value = customer.initial_deposit,
					 	 amount = form.cleaned_data.get('amount'),
					 	 final_value = final_value ,
					 	 transaction = form.cleaned_data.get('transaction'),
					 	 transation_handler = self.request.user)
			transact.save()
			print("1")
			customer.initial_deposit = final_value
			print("2")
			customer.save()
			return redirect("transaction_list")
class Transaction_list(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		transact = BankingHistory.objects.all()
		context = {"banking":transact}
		template_name = "Transact/list.html"
		return render(self.request, template_name, context)

class SavingsTypeDelete(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		savings = SavingType.objects.get(id=self.kwargs['id'])
		savings.delete()
		print("Deleted Savings Type")
		return redirect('savings')
class SavingsType(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		form = SavingsTypeForm()
		context = {"form":form}
		template_name = "savings/create.html"
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		savings = SavingsTypeForm(self.request.POST)
		if savings.is_valid():
			savings.save()
			return redirect("savings")
		context = {"form":form}
		template_name = "savings/create.html"
		return render(self.request, template_name,context)

class SavingsTypeList(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		savings = SavingType.objects.all()
		context = {"savings":savings}
		template_name = "savings/list.html"
		return render(self.request, template_name,context)
class CustomerList(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		customer = Customer.objects.all()
		print(self.request.user.username)
		context = {"Customers":customer}
		template_name = "accounts/customer_list.html"
		return render(self.request, template_name,context)

class CustomerDetail(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		try:
			customer = Customer.objects.get(id=self.kwargs['id'])
		except Customer.DoesNotExist:
			customer = None
		try:
			test = Loan_processing.objects.get(customer=customer)
		except Loan_processing.DoesNotExist:
			test = None
		if test != None:
			loan = True
		else:
			loan = False
		try:
			transact = BankingHistory.objects.filter(customer=customer)
		except BankingHistory.DoesNotExist:
			transact = None
		context = {"form":customer,"loan":loan,"banking":transact}
		template_name = "accounts/customer_detail.html"
		return render(self.request,template_name,context)
class CustomerEdit(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		customer = Customer.objects.get(id=self.kwargs['id'])
		branchs = OCSSC_branch_office.objects.all()
		savings = SavingType.objects.all()
		context = {"form":customer,"branchs":branchs,"savings":savings}
		template_name = "accounts/customer_edit.html"
		return render(self.request,template_name,context)
	def post(self,*args,**kwargs):
		form = CustomerEditForm(self.request.POST,self.request.FILES)
		customer = Customer.objects.get(id=self.kwargs['id'])
		if form.is_valid():
			customer.first_name = form.cleaned_data.get('first_name')
			customer.last_name = form.cleaned_data.get('last_name')
			customer.middle_name = form.cleaned_data.get('middle_name')
			customer.phone_number = form.cleaned_data.get('phone_number')
			customer.address = form.cleaned_data.get('address')
			customer.city = form.cleaned_data.get('city')
			customer.savings_type = SavingType.objects.get(id=self.request.POST['savings_type'])
			customer.office_branch = OCSSC_branch_office.objects.get(id=self.request.POST['office_branch'])
			if 'document' in self.request.FILES:
				customer.document = self.request.FILES['document']
			if 'photograph' in self.request.FILES:
				customer.photograph = self.request.FILES['photograph']
			if 'identification' in self.request.FILES:
				customer.identification = self.request.FILES['identification']
			customer.save()
			return redirect("customer")
		print(form.errors)
		branchs = OCSSC_branch_office.objects.all()
		savings = SavingType.objects.all()
		context = {"form":customer,"branchs":branchs,"savings":savings}
		template_name = "accounts/customer_edit.html"
		return render(self.request,template_name,context)

class CustomerDelete(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		customer = Customer.objects.get(id=self.kwargs['id'])
		customer.delete()
		print("Deleted customer")
		return redirect('customer')
class CustomerCreate(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		Customer = CustomerForm()
		template_name = "accounts/customer_create.html"
		context = {"form":Customer}
		return render(self.request,template_name,context)
	def post(self,*args,**kwargs):
		customer = CustomerForm(self.request.POST,self.request.FILES)
		if customer.is_valid():
			MainCustomer = Customer(	first_name =  customer.cleaned_data.get('first_name'),
				middle_name  =  customer.cleaned_data.get('middle_name'),
				last_name  =   customer.cleaned_data.get('last_name'),
				account_number = customer.cleaned_data.get('account_number'),
				initial_deposit = customer.cleaned_data.get('initial_deposit'),
				phone_number =   customer.cleaned_data.get('phone_number'),
				document =   customer.cleaned_data.get('document'),
				photograph =   customer.cleaned_data.get('photograph') ,
				identification =   customer.cleaned_data.get('identification'),
				address =   customer.cleaned_data.get('address'),
				savings_type = customer.cleaned_data.get('savings_type'),
				city =   customer.cleaned_data.get('city'),
				office_branch =   customer.cleaned_data.get('office_branch'),
				active =    True,
				created_by = self.request.user )
			MainCustomer.save()
			return redirect("customer")

		template_name = "accounts/customer_create.html"
		context = {"form":customer}
		return render(self.request,template_name,context)

class AccountList(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		accounts = User.objects.all()
		context = {"accounts":accounts}
		template_name = "accounts/account_list.html"
		return render(self.request, template_name,context)
class AccountDelete(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		account = User.objects.get(id=self.kwargs['id'])
		account.delete()
		return redirect("account") 

class AccountSuspend(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		account = User.objects.get(id=self.kwargs['id'])
		print("--------") 
		print(account.active)
		print("--------")
		if account.active == True:
			account.active = False
			account.save()
			print("Print - 1 change")
		else:
			account.active = True
			account.save()
			print("Print - 1 change")
		return redirect("account")
class AccountDetail(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		account = User.objects.get(id=self.kwargs['id'])
		context = {"form":account,"detail":True}
		template_name = "accounts/account_create.html"
		return render(self.request, template_name, context)

class AccountEdit(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		accounts=User.objects.get(id=self.kwargs['id']) 
		branchs = OCSSC_branch_office.objects.all()
		position = {('is_manager'), ( 'is_auditor'), ( 'is_customer_service'),( 'is_system_admin')}
		context = {"form":accounts,"branchs":branchs,"position":position}
		template_name = "accounts/account_edit.html"
		return render(self.request, template_name, context)
	def post(self,*args,**kwargs):
		accounts=User.objects.get(id=self.kwargs['id'])
		form = UserCreationUpdateForm(self.request.POST,self.request.FILES)
		if form.is_valid():
			accounts.first_name = form.cleaned_data.get('first_name') 
			accounts.last_name = form.cleaned_data.get('last_name')
			accounts.username = self.request.POST['username']

			accounts.phone_number = form.cleaned_data.get('phone_number')
			accounts.address = form.cleaned_data.get('address')
			accounts.city = form.cleaned_data.get('city')

			user_type = self.request.POST['user_type']			
			accounts.office_branch = form.cleaned_data.get('office_branch')
			if(user_type == "is_manager"):
				accounts.is_manager = True
				accounts.is_auditor = False
				accounts.is_customer_service = False
				accounts.is_system_admin = False
			if(user_type == "is_auditor"):
				accounts.is_auditor = True
				accounts.is_manager = False
				accounts.is_customer_service = False
				accounts.is_system_admin = False
			if(user_type == "is_customer_service"):
				accounts.is_customer_service = True
				accounts.is_auditor = False
				accounts.is_manager = False
				accounts.is_system_admin = False
			if(user_type == "is_system_admin"):
				accounts.is_system_admin = True
				accounts.is_auditor = False
				accounts.is_customer_service = False
				accounts.is_manager = False

			if 'qualification_document' in self.request.FILES:
				accounts.qualification_document = self.request.FILES['qualification_document']		
			if 'photograph' in self.request.FILES:
				accounts.photograph = self.request.FILES['photograph']
			if 'identification' in self.request.FILES:
				accounts.identification = self.request.FILES['identification']
			accounts.save()
			return redirect("account")
		branchs = OCSSC_branch_office.objects.all()
		position = {('is_manager'), ( 'is_auditor'), ( 'is_customer_service'),( 'is_system_admin')}
		context = {"form":form,"branchs":branchs,"position":position}
		template_name = "accounts/account_edit.html"
		return render(self.request, template_name, context)

class Accountnumber(LoginRequiredMixin,View):
	def get_number(self):
		num = AccountNumber.objects.get(id=1)
		return num.accounts

	def post_number(self):
		num = AccountNumber.objects.get(id=1)
		num.accounts = 1+num.accounts
		num.save()
		print("accounts is at "+str(num.accounts))
		return num.accounts

	def get(self,*args,**kwargs):
		print("J working")

		if self.request.is_ajax():
			t = self.post_number()
			print("============")
			print(t)
			t = 100000000+t
			return JsonResponse({'account':t},status=200)

class AccountCreate(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		form = UserCreationForm()
		context = {"form":form,"create":True}
		template_name = "accounts/account_create.html"
		return render(self.request, template_name, context)
	def post(self,*args,**kwargs):
		form = UserCreationForm(self.request.POST,self.request.FILES)
		context = {"form":form,"create":True}
		template_name = "accounts/account_create.html"
		if form.is_valid():
			user = self.request.user
			realDate = self.request.POST['date_of_hire']
			realDate = datetime.datetime.strptime(realDate, '%d/%m/%Y').date()
			print("-------------------------")
			print(form.cleaned_data.get("phone_number"))
			print("-------------------------")
			print("is_valid")
			if(form.cleaned_data.get('position') == "is_manager"):
				is_manager=True
				is_auditor=False
				is_customer_service=False
				is_system_admin=False
			if(form.cleaned_data.get('position') == "is_auditor"):
				is_manager=False
				is_auditor=True
				is_customer_service=False
				is_system_admin=False
			if(form.cleaned_data.get('position') == "is_customer_service"):
				is_manager=False
				is_auditor=False
				is_customer_service=True
				is_system_admin=False
			if(form.cleaned_data.get('position') == "is_system_admin"):
				is_manager=True
				is_auditor=False
				is_customer_service=False
				is_system_admin=True
			user = form.save(user,realDate)
			return redirect("account")
		print("is_not_valid")
		return render(self.request, template_name,context)



from django.shortcuts import render
from django.views import View 
from django.shortcuts import render, redirect

from branchs.models import OCSSC_branch_office
from .models import User
from .forms import UserCreationForm,AbstractUserCreationForm,UserCreationUpdateForm
# Create your views here.

class List(View):
	def get(self,*args,**kwargs):
		accounts = User.objects.all()
		context = {"accounts":accounts}
		template_name = "accounts/list.html"
		return render(self.request, template_name,context)
class Delete(View):
	def get(self,*args,**kwargs):
		account = User.objects.get(id=self.kwargs['id'])
		account.delete()
		return redirect("account") 
class Suspend(View):
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
class Detail(View):
	def get(self,*args,**kwargs):
		account = User.objects.get(id=self.kwargs['id'])
		context = {"form":account}
		template_name = "accounts/create.html"
		return render(self.request, template_name, context)

class Edit(View):
	def get(self,*args,**kwargs):
		accounts=User.objects.get(id=self.kwargs['id'])
		branch = UserCreationUpdateForm
		context = {"form":accounts,"branch":branch}
		template_name = "accounts/edit.html"
		return render(self.request, template_name, context)
class Create(View):
	def get(self,*args,**kwargs):
		form = UserCreationForm()
		context = {"form":form}
		template_name = "accounts/create.html"
		return render(self.request, template_name, context)
	def post(self,*args,**kwargs):
		form = UserCreationForm(self.request.POST,self.request.FILES)
		context = {"form":form}
		template_name = "accounts/create.html"
		if form.is_valid():
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
			user = form.save()
			return redirect("account")
		print("is_not_valid")
		return render(self.request, template_name,context)



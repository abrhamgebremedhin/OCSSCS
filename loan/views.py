from django.shortcuts import render,redirect, get_object_or_404,reverse
from django.views import View 
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Loan_type,Loan_processing,Documents,Conditions
from .forms import LoansTypeForm,LoanApplication,LoanApplicationEdit
from accounts.models import User,Customer
# Create your views here.

class Loan_application_delete(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		loan = Loan_processing.objects.get(id=self.kwargs['id'])
		loan.delete()
		messages.success(self.request, "Deleted a Loan Application Successfully")
		return redirect("loan_application_list")

class Loan_application_unmanager(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		loan = Loan_processing.objects.get(id=self.kwargs['id'])
		loan.approved_by_Manager = False
		loan.save()
		messages.success(self.request, "Auditor "+str(self.request.user)+" Un-approved Loan Application Successfully")
		return redirect(reverse("Loan_application_detail",kwargs={'id':str(self.kwargs['id'])}))

class Loan_application_manager(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		loan = Loan_processing.objects.get(id=self.kwargs['id'])
		loan.approved_by_Manager = True
		loan.manager_approved = self.request.user
		loan.status = 'APPROVED'
		loan.save()
		messages.success(self.request, "Manager "+str(self.request.user)+" Approved Loan Application Successfully")
		return redirect(reverse("Loan_application_detail",kwargs={'id':str(self.kwargs['id'])}))

class Loan_application_unauditor(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		loan = Loan_processing.objects.get(id=self.kwargs['id'])
		loan.approved_by_Auditor = False
		loan.save()
		messages.success(self.request, "Amager "+str(self.request.user)+" Un-approved Loan Application Successfully")
		return redirect(reverse("Loan_application_detail",kwargs={'id':str(self.kwargs['id'])}))

class Loan_application_auditor(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		loan = Loan_processing.objects.get(id=self.kwargs['id'])
		loan.approved_by_Auditor = True
		loan.auditor_approved = self.request.user
		loan.save()
		messages.success(self.request, "Auditor "+str(self.request.user)+" Approved Loan Application Successfully")
		return redirect(reverse("Loan_application_detail",kwargs={'id':str(self.kwargs['id'])}))

class Loan_application_edit(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		loan = Loan_processing.objects.get(id=self.kwargs['id'])
		loan_type = Loan_type.objects.all()
		template_name = "Loan/loan_application/edit.html"
		context = {'form':loan,'Loan_type':loan_type}
		return render(self.request,template_name,context)
	def post(self,*args,**kwargs):
		form = LoanApplicationEdit(self.request.POST,self.request.FILES)
		if form.is_valid():
			loan = Loan_processing.objects.get(id=self.kwargs['id'])
			loan.loan_type = form.cleaned_data.get('loan_type')
			loan.Financial_aid_required = form.cleaned_data.get('Financial_aid_required')
			if 'current_financial_info' in self.request.FILES:
				loan.current_financial_info = self.request.FILES['current_financial_info']
			if 'business_plane' in self.request.FILES:
				loan.business_plane = self.request.FILES['business_plane']
			loan.save()
			for image in self.request.FILES.getlist('images'):
				documents= Documents(loan=loan,image=image )
				documents.save()
			messages.success(self.request, "Edited a Loan Application Successfully")
			return redirect('loan_application_list')
		template_name = "Loan/loan_application/edit.html"
		context = {'form':form}
		return render(self.request,template_name,context)

		

class Loan_application_detail(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		loan = Loan_processing.objects.get(id=self.kwargs['id'])
		if loan.status == "APPROVED":
			return redirect('loan_application_list')
		template_name = "Loan/loan_application/detail.html"
		context = {'form':loan}
		return render(self.request,template_name,context)


class Loan_application_list(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		loan = Loan_processing.objects.filter(status="PENDDING")
		template_name = "Loan/loan_application/list.html"
		context = {'loan':loan,'notapproved':True}
		return render(self.request,template_name,context)

class Loan_application_approved(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		loan = Loan_processing.objects.filter(status="APPROVED")
		template_name = "Loan/loan_application/list.html"
		context = {'loan':loan,'approved':True}
		return render(self.request,template_name,context)

class Loan_application(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		
		
		try:
			customer = Customer.objects.get(id=self.kwargs['id'])
		except Customer.DoesNotExist:
			customer = None
		print("--------------")
		print(customer)
		try:
			test = Loan_processing.objects.get(customer=customer)
		except Loan_processing.DoesNotExist:
			test = None
		print("--------------")
		print(test)
		if test != None:
			customer = Customer.objects.all()
			context = {"Customers":customer}
			template_name = "accounts/customer_list.html"
			messages.error(self.request, "Loan Applications already existes")
			return redirect("customer")

		loan = LoanApplication()
		template_name = "Loan/loan_application/create.html"
		context = {'form':loan}
		return render(self.request,template_name,context)
	def post(self,*args,**kwargs):	
		form = LoanApplication(self.request.POST,self.request.FILES)
		if form.is_valid():
			loan_application = Loan_processing(	
				status = "PENDDING",
				customer = Customer.objects.get(id=self.kwargs['id']),
				loan_type = form.cleaned_data.get('loan_type'),
				current_financial_info = form.cleaned_data.get('current_financial_info'),
				business_plane = form.cleaned_data.get('business_plane'),
				Financial_aid_required = form.cleaned_data.get('Financial_aid_required'),
				rejected_by_manager = False,
				rejected_by_customer = False,
				approved_by_Auditor = False,
				create_by = self.request.user)
			loan_application.save()
			for image in self.request.FILES.getlist('images'):
				documents= Documents(loan=loan_application,image=image )
				documents.save()
			return redirect("loan_application_list")
		template_name = "Loan/loan_application/create.html"
		context = {'form':loan}
		return render(self.request,template_name,context)


class Loan_type_delete(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		loan = Loan_type.objects.get(id=self.kwargs['id'])
		loan.delete()
		return redirect("loan_type_list")

class Loan_type_list(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		loan = Loan_type.objects.all()
		template_name = "Loan/loan_type/list.html"
		context = {'types':loan}
		return render(self.request,template_name,context)

class Loan_type_edit(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		loan = Loan_type.objects.get(id=self.kwargs['id'])
		template_name = "Loan/loan_type/edit.html"
		context = {'form':loan}
		return render(self.request,template_name,context)

	def post(self,*args,**kwargs):
		loan = LoansTypeForm(self.request.POST)
		if loan.is_valid():

			old_loan = Loan_type.objects.get(id=self.kwargs['id'])
			old_loan.name=loan.cleaned_data.get('name')
			old_loan.detail=loan.cleaned_data.get('detail')
			old_loan.save()
			return redirect("loan_type_list")

		template_name = "Loan/loan_type/edit.html"
		context = {'form':loan}
		return render(self.request,template_name,context)

class Loan_type_create(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		loan = LoansTypeForm()
		template_name = "Loan/loan_type/create.html"
		context = {'form':loan}
		return render(self.request,template_name,context)
	def post(self,*args,**kwargs):
		loan = LoansTypeForm(self.request.POST)
		if loan.is_valid():
			loan.save()
			return redirect("loan_type_list")

		template_name = "Loan/loan_type/create.html"
		context = {'form':loan}
		return render(self.request,template_name,context)








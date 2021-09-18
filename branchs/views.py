from django.shortcuts import render
from django.views import View 
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import BranchForm
from .models import OCSSC_branch_office
from accounts.models import User
# Create your views here.



class Home(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		template_name="branchs/list.html"
		branchs = OCSSC_branch_office.objects.all()
		context = {'branch_list':branchs}
		return render(self.request, template_name,context)

class Create(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		form = BranchForm()
		template_name="branchs/create.html"
		context = {'form':form,}
		return render(self.request, template_name, context)
	def post(self,*args,**kwargs):
		form = BranchForm(self.request.POST)
		if form.is_valid():
			branch = form.save(commit=False)
			branch.save()
			print("Success 1")
			return redirect("Branch")
		#messages.error(self.request, "some thing went wrong")
		return redirect("Branch_create")
class Edit(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		form = OCSSC_branch_office.objects.get(id=self.kwargs['id'])
		user = User.objects.all()
		template_name="branchs/edit.html"
		context = {'form':form,"user":user}
		return render(self.request, template_name, context)
	def post(self,*args,**kwargs):
		form = BranchForm(self.request.POST)
		id = self.kwargs['id']
		user = User.objects.all()
		branch = OCSSC_branch_office.objects.get(id=self.kwargs['id'])
		if form.is_valid():
			print("Success 2")
			branch.name = form.cleaned_data.get('name')
			branch.city = form.cleaned_data.get('city')
			branch.address = form.cleaned_data.get('address')
			branch.head_office = form.cleaned_data.get('head_office')
			branch.manager = form.cleaned_data.get('manager')
			branch.save()
			return redirect("Branch")
		#messages.error(self.request, "some thing went wrong")
		print("Success 1")
		user = User.objects.all()
		template_name="branchs/edit.html"
		context = {'form':form,"user":user}
		return render(self.request, template_name, context)

class Delete(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		branch = OCSSC_branch_office.objects.get(id=self.kwargs['id'])
		branch.delete()
		return redirect("Branch") 

		'''
		form = AnnouncementForm(self.request.POST,self.request.FILES) 
		try:
			if form.is_valid():
				announcement = form.save(commit=False)
				announcement.created_by = self.request.user  
				announcement.save()
				for image in self.request.FILES.getlist('images'):
					announcementimage= AnnouncementImages( announcement=announcement, image = image )
					announcementimage.save()
				messages.success(self.request, "Added New Announcement Successfully")
				return redirect("admin:anounce_list")
		'''
		"""
		class CreatBlog(LoginRequiredMixin,View):
	def get(self,*args,**kwargs):
		form = BlogsForm()
		template_name="admin/pages/blog_form.html"
		context={'form':form}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = BlogsForm(self.request.POST,self.request.FILES)
		import pprint
		pprint.pprint(self.request.FILES)
		context={'form':form}
		if form.is_valid():
			# the data we need for cropping
			x = self.request.POST.get('x')
			y = self.request.POST.get('y')
			w = self.request.POST.get('width')
			h = self.request.POST.get('height')

			# Where the cropping is done
			blog = form.save(self.request.user,x,y,w,h)
			messages.success(self.request, "Added New Blog Successfully")
			return redirect("admin:admin_Blogs")
		return render(self.request, "admin/pages/blog_form.html",context)
		
		"""
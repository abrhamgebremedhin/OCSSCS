from django.contrib import admin
from functools import update_wrapper
from django.template.response import TemplateResponse
from django.urls import path,include

from accounts.forms import AdminLoginForm

class CustomAdminSite(admin.AdminSite):
    login_form = AdminLoginForm
    def get_urls(self):
        urls = super().get_urls()
      
        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            wrapper.admin_site = self
            return update_wrapper(wrapper, view)

        my_urls = []
                
        return my_urls + urls


admin_site = CustomAdminSite(name='myadmin')
# Register your models here.

from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class CustomAdminAppConfig(AdminConfig):
    default_site = "accounts.admin.CustomAdminSite"

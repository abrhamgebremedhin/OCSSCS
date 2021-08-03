from django.urls import path,include

from .views import Home,Create,Edit,Delete
                    

urlpatterns = [ 
    path('',Home.as_view(),name='Branch'),
    path('create',Create.as_view(),name='Branch_create'),
    path('Edit/<id>',Edit.as_view(),name='Branch_edit'),
    path('Delete/<id>',Delete.as_view(),name='Branch_delete'),
    ]
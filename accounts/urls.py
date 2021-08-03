from django.urls import path,include

from .views import List,Create,Edit,Delete,Suspend,Detail
                    

urlpatterns = [ 
    path('',List.as_view(),name='account'),
    path('account_create',Create.as_view(),name='account_create'),
    path('account_edit/<id>',Edit.as_view(),name='account_edit'),
    path('account_delete/<id>',Delete.as_view(),name='account_delete'),
    path('account_suspend/<id>',Suspend.as_view(),name='account_suspend'),
    path('account_detail/<id>',Detail.as_view(),name='account_detail'),
    ]
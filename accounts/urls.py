from django.urls import path,include

from .views import (LoginView,Accountnumber,AccountList,AccountCreate,AccountEdit,AccountDelete,AccountSuspend,AccountDetail
					,CustomerList,CustomerCreate,CustomerDelete,CustomerDetail,CustomerEdit,Transact,Transaction_list,
                    SavingsType,SavingsTypeList,SavingsTypeDelete,)
                    

urlpatterns = [ 

    path("",include("django.contrib.auth.urls")),
    path("user-login/",LoginView.as_view(),name="cm_login"),

    path('account_list',AccountList.as_view(),name='account'),
    path('customer_create/account_number',Accountnumber.as_view(),name='account_number'),
    path('account_create',AccountCreate.as_view(),name='account_create'),
    path('account_edit/<id>',AccountEdit.as_view(),name='account_edit'),
    path('account_delete/<id>',AccountDelete.as_view(),name='account_delete'),
    path('account_suspend/<id>',AccountSuspend.as_view(),name='account_suspend'),
    path('account_detail/<id>',AccountDetail.as_view(),name='account_detail'),

    path('customer_list/',CustomerList.as_view(),name='customer'),
    path('customer_create/',CustomerCreate.as_view(),name='customer_create'),
    path('customer_delete/<id>',CustomerDelete.as_view(),name='customer_delete'),
    path('customer_detail/<id>',CustomerDetail.as_view(),name='customer_detail'),
    path('customer_edit/<id>',CustomerEdit.as_view(),name='customer_edit'),

    path('savings_create',SavingsType.as_view(),name='savings_create'),
    path('savings_list',SavingsTypeList.as_view(),name='savings'),
    path('savings_delete/<id>',SavingsTypeDelete.as_view(),name='savings_delete'),

    path('transact/<id>',Transact.as_view(),name='transact'),
    path('transact-list/',Transaction_list.as_view(),name='transaction_list'),
    
    ]
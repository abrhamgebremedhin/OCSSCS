from django.urls import path,include

from .views import (Loan_type_list,Loan_type_create,Loan_type_edit,Loan_type_delete,
					Loan_application,Loan_application_list,Loan_application_detail,Loan_application_edit,
					Loan_application_delete,Loan_application_approved,Loan_application_auditor,
					Loan_application_unauditor,Loan_application_unmanager,Loan_application_manager)
                    

urlpatterns = [ 
    path('loan_type_create',Loan_type_create.as_view(),name='loan_type_create'),
    path('loan_type_list',Loan_type_list.as_view(),name='loan_type_list'),
    path('laon_type_edit/<id>',Loan_type_edit.as_view(),name='Loan_type_edit'),
    path('laon_type_delete/<id>',Loan_type_delete.as_view(),name='Loan_type_delete'),

    path('loan_application/<id>',Loan_application.as_view(),name='loan_application'),
    path('loan_application_list',Loan_application_list.as_view(),name='loan_application_list'), 
    path('loan_application_approved',Loan_application_approved.as_view(),name='loan_application_approved'), 
    path('loan_application_detail/<id>',Loan_application_detail.as_view(),name='Loan_application_detail'),
    path('Loan_application_manager/<id>',Loan_application_manager.as_view(),name='loan_application_manager'),
    path('Loan_application_unmanager/<id>',Loan_application_unmanager.as_view(),name='loan_application_unmanager'),
    path('loan_application_auditor/<id>',Loan_application_auditor.as_view(),name='Loan_application_auditor'),
    path('loan_application_unauditor/<id>',Loan_application_unauditor.as_view(),name='Loan_application_unauditor'),
    path('loan_application_edit/<id>',Loan_application_edit.as_view(),name='Loan_application_edit'),
    path('loan_application_delete/<id>',Loan_application_delete.as_view(),name='Loan_application_delete'),


    

    ]
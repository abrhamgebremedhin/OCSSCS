from django.urls import path,include

from .views import Home,Create,Edit,Delete
                    

urlpatterns = [ 
    path('',Home.as_view(),name=''),
    path('create',Create.as_view(),name='create'),
    path('Edit/<id>',Edit.as_view(),name='Edit'),
    path('Delete/<id>',Delete.as_view(),name='Delete'),
    ]
from django.urls import path

from call.views import *

urlpatterns = [
    path('', index, name='index'),
    path('get_user_details/', get_user_details, name='get_user_details')
    # path('another_page/', views.another_page, name='another_page'),
]
from django.urls import path
from authentication.views import *


urlpatterns = [
    path("",UserLogin,name="login"),
    path("register/",UserRegister,name="register"),
    path("suceess/",Suceess,name="Suceess"),
    path("token_send/",token_send,name="token_send"),
    path('registration_varify/<auth_token>',RegistrationVarify,name="varify"),
    path("update_profile/",UpdateProfile,name="UpdateProfile"),
    
]

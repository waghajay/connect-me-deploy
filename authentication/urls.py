from django.urls import path
from authentication.views import *
from authentication.form import MyPasswordResetForm , MyPasswordForm
from django.contrib.auth.views import PasswordResetView , PasswordResetConfirmView , PasswordResetDoneView , PasswordResetCompleteView

urlpatterns = [
    path("",UserLogin,name="login"),
    path("register/",UserRegister,name="register"),
    path("suceess/",Suceess,name="Suceess"),
    path("token_send/",token_send,name="token_send"),
    path('registration_varify/<auth_token>',RegistrationVarify,name="varify"),
    path("update_profile/",UpdateProfile,name="UpdateProfile"),    
    
    # Password Reset Views    
    path("reset-password/",PasswordResetView.as_view(template_name="authentication/reset-password.html",form_class=MyPasswordResetForm),name="reset-password"),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(template_name="authentication/reset-password-confirm.html" , form_class=MyPasswordForm),name="password_reset_confirm"),
    path("password-reset-done/",PasswordResetDoneView.as_view(template_name="authentication/reset-password-done.html"),name="password_reset_done"),
    path("password-reset-complete/",PasswordResetCompleteView.as_view(template_name="authentication/password-reset-complete.html"),name="password_reset_complete")   
    
]

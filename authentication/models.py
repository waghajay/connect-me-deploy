from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=40,null=True,blank=True)
    otp = models.CharField(max_length=10,null=True,blank=True)
    otp_expiration_time = models.DateTimeField(null=True,blank=True)
    auth_token = models.CharField(max_length=100,default="")
    is_varified = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=20,null=True,blank=True)
    user_bio = models.TextField(max_length=100,null=True,blank=True)
    Gender = (
        ('Male','Male'),
        ('Female','Female'),
        ('Prefer_Not_Say', "Prefer Not Say")
    )
    gender = models.CharField(max_length=30,choices=Gender,null=True,blank=True)
    address = models.CharField(max_length=250,null=True,blank=True)
    account_created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", default="profile_pictures/profile_image.jpeg")
    cover_picture = models.ImageField(upload_to="cover_pictures/", default="profile_pictures/cover_image.jpeg")
    friends = models.ManyToManyField(User, related_name='friends',null=True,blank=True)
    Online_Status = (
        ('Online','Online'),
        ('Offline','Offline')
    )
    online_status = models.CharField(max_length=30,choices=Online_Status,null=True,blank=True,default="Offline")
    
    def __str__(self):
        return f"Username :- {self.username} ---- Email:- {self.user.email}"
    
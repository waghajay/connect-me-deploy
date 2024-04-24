from django.db import models
from authentication.models import UserProfile
from django.contrib.auth.models import User

# Create your models here.


class Friendship(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True,blank=True)
    from_user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    is_friend = models.BooleanField(null=True,blank=True,default=False)
    accepted_at = models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return f"{self.from_user} ..... {self.to_user} ..... Is Friend:- {self.is_friend}"
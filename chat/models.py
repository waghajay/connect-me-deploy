from django.db import models
from django.contrib.auth.models import User

# Create your models here.    
    
class Room(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
    users = models.ManyToManyField(User, related_name='room_user_list',null=True,blank=True)    
    
    def __str__(self):
        return self.name
    


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE,null=True,blank=True)
    content = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='message_images/', blank=True, null=True)
    date_added = models.DateField(null=True,blank=True)
    time = models.TimeField(auto_now_add=True,null=True,blank=True)

    class Meta:
        ordering = ('date_added',)
        
    def __str__(self):
        return f"Message :-{self.content} ----- User:- {self.user} ----- Room:- {self.room}" 
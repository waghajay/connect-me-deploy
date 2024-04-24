from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from authentication.models import UserProfile
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from friendship_app.models import Friendship
from chat.models import Room
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import random
import uuid



# Create your views here.

def Profile(request,username):
    user = str(request.user)
    user_profile = get_object_or_404(UserProfile, user__last_name=username)
    user_email = user_profile.user.email  
    
    request_check = Friendship.objects.filter(from_user=request.user, to_user=user_profile.user) 
    check_is_request_exitst_or_not = Friendship.objects.filter(from_user=user_profile.user,to_user=request.user).first()   
    request_check_status = Friendship.objects.filter(from_user=request.user, to_user=user_profile.user).first() 
    
    if check_is_request_exitst_or_not:
        if check_is_request_exitst_or_not.status == "pending":
            return render(request,"friendship_app/profile.html",{ "user_profile" : user_profile,"friend_request_status" : "Accept" })
        if check_is_request_exitst_or_not.status == "accepted": 
            return render(request,"friendship_app/profile.html",{ "user_profile" : user_profile,"friend_request_status" : "Message" })
    
    if user==user_email:
        return render(request,"friendship_app/profile.html",{ "user_profile" : user_profile,"authenticated_user" : "user" })
    
    if not request_check.exists():
        return render(request,"friendship_app/profile.html",{ "user_profile" : user_profile,"friend_request_status" : "Send Request" })
    
    if request_check_status.status == "pending":
        return render(request,"friendship_app/profile.html",{ "user_profile" : user_profile,"friend_request_status" : "Request Send" })
        
    elif request_check_status.status == "accepted":
        return render(request,"friendship_app/profile.html",{ "user_profile" : user_profile,"friend_request_status" : "Message" })

    else:
        return render(request,"friendship_app/profile.html",{ "user_profile" : user_profile,"friend_request_status" : "Send Request Again" })
    
    return render(request,"friendship_app/profile.html",{ "user_profile" : user_profile })



@csrf_exempt
def send_request(request, to_user_id):
    if request.method == 'POST':        
        from_user = request.user
        to_user = User.objects.get(id=to_user_id)        
        user_profile = UserProfile.objects.filter(user=to_user).first()
        
        Friendship.objects.create(user=user_profile,from_user=from_user, to_user=to_user,status="pending")
        
        username = to_user.last_name
       
        return redirect(reverse('profile', args=[username]))
    else:
        pass

def accept_request(request, to_user_id):
    from_user = request.user
    to_user = User.objects.get(id=to_user_id)
    
    from_user_profile = get_object_or_404(UserProfile, user=from_user)
    from_user_profile.friends.add(to_user)

    from_user_profile = get_object_or_404(UserProfile, user=to_user)
    from_user_profile.friends.add(from_user)

    generated_room_id = random.randint(1111,9999999999999999)
        
    room_name = str(uuid.uuid4())
    
    room = Room.objects.create(name=room_name,slug=room_name)
    room.users.add(from_user,to_user)
    
    
    friend_request = Friendship.objects.filter(from_user=to_user, to_user=from_user, is_friend=False).first()
    
    if friend_request:
        
        friend_request.is_friend = True
        friend_request.status = "accepted"
        friend_request.accepted_at = timezone.now()
        friend_request.save()
        
        return HttpResponse("Friend request accepted successfully!")
    
    else:
        return HttpResponse("No pending friend request found.")
    
    
def reject_request(request, to_user_id):
    from_user = request.user
    to_user = User.objects.get(id=to_user_id)
    
    friend_request = Friendship.objects.filter(from_user=to_user, to_user=from_user, is_friend=False).first()
    
    if friend_request:
        
        friend_request.is_friend = False
        friend_request.status = "rejected"
        friend_request.delete()
        
        return HttpResponse("Friend request rejected successfully!")
    
    else:
        return HttpResponse("No pending friend request found.")
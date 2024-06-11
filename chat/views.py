from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from authentication.models import UserProfile
from django.db.models import Q
from friendship_app.models import Friendship
from chat.models import Room,Message
from django.contrib.auth.models import User

# Create your views here.

@login_required(login_url="login")
def Index(request):
    user = request.user
    user_profile = UserProfile.objects.filter(user=user).first()
    username = user_profile.user.first_name
    
    check_requests = Friendship.objects.filter(to_user=user, status="pending").all()
    
    friends = user_profile.friends.all()
    
    return render(request, "chat/chat.html", {"username": username, "requests": check_requests, "user_profile": user_profile,"friends": friends})


@login_required(login_url="login")  
def search_users(request):
    query = request.GET.get('query', '')
    if query:
        profiles = UserProfile.objects.filter(
            Q(username__icontains=query) | Q(user__first_name__icontains=query)
        )
        results = [{'username': profile.username, 'email': profile.user.email, 'name': profile.user.first_name, 'profile_picture': profile.profile_picture.url, 'cover_picture': profile.cover_picture.url} for profile in profiles]
    else:
        results = []
    return JsonResponse({'results': results})


@login_required(login_url="login")  
def get_friend_info(request, friend_id):
    try:
        
        user = request.user
        
        user_user = User.objects.filter(username=user).first()
        
        friend = UserProfile.objects.get(user=friend_id)
        current_user = request.user

        room = Room.objects.filter(users=current_user).filter(users=friend.user).first()
        room_name = room.name if room else None


        friend_info = {
            'first_name': friend.user.first_name,
            'id': friend.user.id,
            'last_name': friend.user.last_name,
            'email': friend.user.email, 
            'profile_picture': friend.profile_picture.url,
            'room_name': room_name,
            'username': user_user.email,
            'another_user_username' : friend.user.email
            
        }

        return JsonResponse({'friendInfo': friend_info})
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Friend not found'}, status=404)
    
    

  # Assuming you have a Message model defined

# @login_required(login_url="login")  
def get_messages_for_room(request, room_name):
    try:
        # Query messages from the database based on the room_name
        messages = Message.objects.filter(room__name=room_name)
        
        
        messages_list = []
        for message in messages:
            message_dict = {
                'content': message.content,
                'username': message.user.username,
                'image_url': message.image.url if message.image else None,
                'time' : message.time,
            }
            messages_list.append(message_dict)
        
        # Return the messages as JSON response
        return JsonResponse({'messages': messages_list})
    except Message.DoesNotExist:
        # If no messages found, return a JSON response with error message and status 404
        return JsonResponse({'error': 'Messages not found'}, status=404)


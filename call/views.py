from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from authentication.models import UserProfile
# Create your views here.
# def index(request):
#     return render(request, 'call/index.html')



def index(request):
    # Retrieve the name from the session
    other_user_name = request.session.get('other_user_name')
    
    # Assuming `other_user_name` contains the last name of the user
    # Filter the User objects based on last name
    users_with_last_name = User.objects.filter(last_name=other_user_name)
    
    # Assuming there's only one user with the given last name
    # If there could be multiple users, handle the queryset accordingly
    if users_with_last_name.exists():
        # Get the first user from the queryset
        first_user = users_with_last_name.first()
        # Access the first name of the user
        first_name = first_user.first_name
        print(first_name)  # Print the first name of the user
        # Clear the session data to avoid keeping it after it's been used
        request.session.pop('other_user_name', None)
        # You can pass the first name to the template for rendering
        return render(request, 'call/index.html', {'other_user_name': other_user_name, 'first_name': first_name})
    else:
        # Handle the case where no user is found with the given last name
        # For example, return an error message or redirect to an error page
        return render(request, 'call/index.html', {'message': 'User not found'})






def get_user_details(request):
    user_id = request.GET.get('userId')
    user = User.objects.get(id=user_id)
    # Retrieve user details as needed
    # For example:
    user_profile = UserProfile.objects.get(user=user)
    # Store the name in the session
    request.session['other_user_name'] = user_profile.user.last_name
    # Perform any other operations if needed
    return JsonResponse({'status': 'success'})
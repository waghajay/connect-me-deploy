from django.urls import path
from friendship_app.views import Profile,send_request,accept_request,reject_request

urlpatterns = [
    path("@<str:username>/", Profile, name="profile"),
    path('send_request/<int:to_user_id>/', send_request, name='send_request'),
    path('accept_request/<int:to_user_id>/',accept_request,name="accept_request"),
    path('reject_request/<int:to_user_id>/',reject_request,name="reject_request")
]

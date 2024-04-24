from django.urls import path
from chat.views import *

urlpatterns = [
    path("",Index,name="ChatIndex"),
    path("chat/@<str:username>",ChatPage,name="ChatPage"),
    path("search/", search_users, name='search_users'),
    path('get_friend_info/<int:friend_id>/', get_friend_info, name='get_friend_info'),
    path('get_messages_for_room/<str:room_name>/', get_messages_for_room, name='get_messages_for_room'),

]

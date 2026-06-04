from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent, name='sent'),
    path('compose/', views.compose, name='compose'),
    path('chat/<int:user_id>/', views.chat_room, name='chat_room'),
    path('delete/<int:pk>/', views.delete_message, name='delete'),
]

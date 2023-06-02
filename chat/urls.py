# urls.py
from django.urls import path
from chat.views import chat_index, chat_window, chat_refresh

urlpatterns = [
    path('chat/', chat_index, name='chat_index'),
    path('chat/window/<int:recipient_id>/', chat_window, name='chat_window'),
    path('chat/refresh/', chat_refresh, name='chat_refresh'),
]

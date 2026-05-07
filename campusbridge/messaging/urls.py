from django.urls import path
from .views import chat,send_message
urlpatterns=[path('chat/<int:convo_id>/',chat,name='chat'),
             path('send/<int:convo_id>/',send_message,name='send_message')]
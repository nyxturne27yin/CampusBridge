from django.urls import path
from . import views
urlpatterns=[path('chat/<int:convo_id>/',views.chat,name='chat'),
             path('send/<int:convo_id>/',views.send_message,name='send_message'),
             path('', views.conversation_list, name='conversation_list'),
             path('start/<int:counselor_id>/', views.start_conversation, name='start_conversation'),]
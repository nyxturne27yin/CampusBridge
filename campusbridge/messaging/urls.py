from django.urls import path
from . import views
urlpatterns=[path('chat/<int:convo_id>/',views.chat,name='chat'),
             path('send/<int:convo_id>/',views.send_message,name='send_message'),
             path('', views.conversation_list, name='conversation_list'),
             path('start/<int:counselor_id>/', views.start_conversation, name='start_conversation'),
             # 👇 ADD THESE
             path("inbox/", views.counselor_inbox, name="counselor_inbox"),
             path("student/inbox/", views.student_inbox, name="student_inbox"),

             path("delete/<int:conversation_id>/", views.delete_conversation, name="delete_conversation")
             ]
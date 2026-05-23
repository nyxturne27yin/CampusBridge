from django.urls import path
from .views import create_request, my_request, counselor_requests, update_request, delete_request,track_requests

urlpatterns = [
    path('create/', create_request, name='create_request'),
    path('my/', my_request, name='my_request'),
    path('counselor/', counselor_requests, name='counselor_requests'),
    path('requests/', my_request, name='support_requests'),
    path('request/update/<int:pk>/', update_request, name='update_request'),
    path('request/delete/<int:pk>/', delete_request, name='delete_request'),
path('request/track/', track_requests, name='track_requests'),
]

from django.urls import path
from .views import create_request, my_request, counselor_requests

urlpatterns = [
    path('create/', create_request, name='create_request'),
    path('my/', my_request, name='my_request'),
    path('counselor/', counselor_requests, name='counselor_requests'),
path('requests/', my_request, name='support_requests'),
]
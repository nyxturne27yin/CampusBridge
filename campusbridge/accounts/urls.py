from django.urls import path
from .views import *

urlpatterns = [

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),

    path('dashboard/student/', student_dashboard, name='student_dashboard'),
    path('dashboard/staff/', staff_dashboard, name='staff_dashboard'),
    path('dashboard/counselor/', counselor_dashboard, name='counselor_dashboard'),
]
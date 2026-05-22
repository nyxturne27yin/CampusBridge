from django.contrib import admin
from django.urls import path, include
from accounts.views import (
    home,
    register_view,
    login_view,
    logout_view,
    dashboard_redirect,
    student_dashboard,
    counselor_dashboard,
    staff_dashboard
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/student/', student_dashboard, name='student_dashboard'),
    path('dashboard/counselor/', counselor_dashboard, name='counselor_dashboard'),
    path('dashboard/staff/', staff_dashboard, name='staff_dashboard'),

    path('support/', include('support.urls')),
    path('messaging/', include('messaging.urls')),
    path('appointments/', include('appointments.urls')),
]
from django.urls import path
from .views import create_slot,view_slots,book_slot,manage_appointments,update_appointment

urlpatterns = [
    path('create/', create_slot, name='create_slot'),
    path('slots/', view_slots, name='view_slots'),
    path('book/<int:slot_id>/', book_slot, name='book_slot'),
    path('manage/', manage_appointments, name='manage_appointments'),
    path('update/<int:app_id>/<str:status>/', update_appointment, name='update_appointment'),
]
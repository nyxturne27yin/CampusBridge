from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from messaging.models import Conversation
from datetime import datetime, date, timedelta, time

from accounts.models import User
from .models import CounselorAvailability, Notification, Appointment
from support.models import AnonymousProfile


def generate_slots_for_counselor(counselor):
    start_date = date.today()

    for d in range(7):
        day = start_date + timedelta(days=d)

        for hour in range(10, 17):
            CounselorAvailability.objects.get_or_create(
                counselor=counselor,
                date=day,
                time_slot=time(hour, 0),
                defaults={"is_booked": False}
            )


@login_required
def create_slot(request):
    if request.method == "POST":
        slot_date = request.POST.get('date')
        slot_time = request.POST.get('time_slot')

        if not slot_date or not slot_time:
            messages.error(request, "Date and time are required")
            return redirect('create_slot')

        try:
            slot_date_obj = datetime.strptime(slot_date, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format")
            return redirect('create_slot')

        if slot_date_obj < date.today():
            messages.error(request, "Cannot create past slots")
            return redirect('create_slot')

        exists = CounselorAvailability.objects.filter(
            counselor=request.user,
            date=slot_date_obj,
            time_slot=slot_time
        ).exists()

        if exists:
            messages.error(request, "Slot already exists")
            return redirect('create_slot')

        CounselorAvailability.objects.create(
            counselor=request.user,
            date=slot_date_obj,
            time_slot=slot_time
        )

        messages.success(request, "Slot created successfully")
        return redirect('view_slots')

    return render(request, 'appointments/create_slot.html')


@login_required
def view_slots(request):

    counselors = User.objects.filter(role="counselor")

    for counselor in counselors:
        generate_slots_for_counselor(counselor)

    slots = CounselorAvailability.objects.filter(
        is_booked=False,
        date__gte=date.today()
    ).order_by("date", "time_slot")

    return render(request, "appointments/slots.html", {
        "slots": slots
    })
@login_required
def book_slot(request, slot_id):
    slot = get_object_or_404(CounselorAvailability, id=slot_id, is_booked=False)

    slot.is_booked = True
    slot.save()

    Appointment.objects.create(
        slot=slot,
        counselor=slot.counselor,
        anonymous_profile=request.user.anonymousprofile,
        status="pending"
    )

    Notification.objects.create(
        user=slot.counselor,
        message=f"New appointment booked by {request.user.username}"
    )

    return redirect("view_slots")


@login_required
def manage_appointments(request):
    appointments = Appointment.objects.filter(
        counselor=request.user
    ).select_related('anonymous_profile', 'slot', 'slot__counselor')

    return render(request, "appointments/manage.html", {
        "appointments": appointments
    })


ALLOWED_STATUS = ["pending", "approved", "rejected"]


@login_required
def update_appointment(request, app_id, status):

    if status not in ["pending", "approved", "rejected"]:
        messages.error(request, "Invalid status")
        return redirect('manage_appointments')

    app = get_object_or_404(
        Appointment,
        id=app_id,
        counselor=request.user
    )

    app.status = status
    app.save()

    if status == "approved":
        Conversation.objects.get_or_create(
            anonymous_profile=app.anonymous_profile,
            counselor=app.counselor
        )

    send_mail(
        "Appointment Status Update",
        f"Your appointment is now {status}",
        "system@campusbridge.com",
        [app.anonymous_profile.user.email],
        fail_silently=True
    )

    messages.success(request, "Status updated successfully")
    return redirect('manage_appointments')
@login_required
def counselor_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "appointments/notifications.html", {
        "notifications": notifications
    })


@login_required
def counselor_dashboard(request):
    if request.user.role == "counselor":
        generate_slots_for_counselor(request.user)

    return render(request, "dashboard/counselor.html")
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CounselorAvailability, Appointment
from support.models import AnonymousProfile
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime, date
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
    slots = CounselorAvailability.objects.filter(
        is_booked=False,
        date__gte=date.today()
    ).order_by("date", "time_slot")

    return render(request, "appointments/slots.html", {
        "slots": slots
    })

@login_required
def book_slot(request, slot_id):
    slot = get_object_or_404(
        CounselorAvailability,
        id=slot_id,
        is_booked=False
    )

    anon, created = AnonymousProfile.objects.get_or_create(
        user=request.user
    )

    Appointment.objects.create(
        slot=slot,
        counselor=slot.counselor,
        anonymous_profile=anon
    )

    slot.is_booked = True
    slot.save()

    return redirect('view_slots')


@login_required
def manage_appointments(request):
    appointments = Appointment.objects.filter(
        counselor=request.user
    ).select_related('anonymous_profile', 'slot')

    return render(request, 'appointments/manage.html', {
        'appointments': appointments
    })


from django.contrib import messages

ALLOWED_STATUS = ["pending", "approved", "rejected"]

@login_required
def update_appointment(request, app_id, status):

    if status not in ALLOWED_STATUS:
        messages.error(request, "Invalid status")
        return redirect('manage_appointments')

    app = get_object_or_404(
        Appointment,
        id=app_id,
        counselor=request.user
    )

    app.status = status
    app.save()

    send_mail(
        "Appointment Status Update",
        f"Your appointment is now {status}",
        "system@campusbridge.com",
        [app.anonymous_profile.user.email],
        fail_silently=True
    )

    messages.success(request, "Status updated successfully")
    return redirect('manage_appointments')
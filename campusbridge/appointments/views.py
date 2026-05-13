from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CounselorAvailability, Appointment
from support.models import AnonymousProfile
from django.core.mail import send_mail


@login_required
def create_slot(request):
    if request.method == "POST":
        CounselorAvailability.objects.create(
            counselor=request.user,
            date=request.POST['date'],
            time_slot=request.POST['time_slot']
        )
        return redirect('view_slots')

    return render(request, 'appointments/create_slot.html')


@login_required
def view_slots(request):
    slots = CounselorAvailability.objects.filter(is_booked=False)
    return render(request, 'appointments/slots.html', {
        'slots': slots
    })

@login_required
def book_slot(request, slot_id):
    slot = get_object_or_404(
        CounselorAvailability,
        id=slot_id,
        is_booked=False
    )

    anonymous_profile = get_object_or_404(
        AnonymousProfile,
        user=request.user
    )

    Appointment.objects.create(
        anonymous_profile=anonymous_profile,
        counselor=slot.counselor,
        slot=slot
    )

    slot.is_booked = True
    slot.save()

    return redirect('view_slots')


@login_required
def manage_appointments(request):
    appointments = Appointment.objects.filter(counselor=request.user)

    return render(request, 'appointments/manage.html', {
        'appointments': appointments
    })


@login_required
def update_appointment(request, app_id, status):

    app = get_object_or_404(
        Appointment,
        id=app_id
    )

    if app.counselor == request.user:

        app.status = status
        app.save()

        send_mail(
            "Appointment Status Update",
            f"Your appointments is now {status}",
            "system@campusbridge.com",
            [app.anonymous_profile.user.email],
            fail_silently=True
        )

    return redirect('manage_appointments')

def appointments_home(request):
    return redirect('view_slots')
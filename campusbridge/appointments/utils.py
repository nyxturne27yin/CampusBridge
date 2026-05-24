from datetime import date, timedelta, time
from .models import CounselorAvailability
from accounts.models import User


def generate_slots_for_counselor(counselor, days_ahead=7):

    last_slot = CounselorAvailability.objects.filter(
        counselor=counselor
    ).order_by("-date", "-time_slot").first()

    # Determine start date
    if last_slot:
        start_date = last_slot.date + timedelta(days=1)
    else:
        start_date = date.today()

    created_count = 0


    for i in range(days_ahead):
        current_date = start_date + timedelta(days=i)

        for hour in range(9, 17):
            obj, created = CounselorAvailability.objects.get_or_create(
                counselor=counselor,
                date=current_date,
                time_slot=time(hour, 0)
            )

            if created:
                created_count += 1

    return created_count
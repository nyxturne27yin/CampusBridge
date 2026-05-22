from datetime import date, timedelta, time
from .models import CounselorAvailability
from accounts.models import User


def generate_slots_for_counselor(counselor):
    today = date.today()

    for i in range(7):  # next 7 days
        d = today + timedelta(days=i)

        for hour in range(9, 17):  # 9 AM - 5 PM
            CounselorAvailability.objects.get_or_create(
                counselor=counselor,
                date=d,
                time_slot=f"{hour}:00"
            )
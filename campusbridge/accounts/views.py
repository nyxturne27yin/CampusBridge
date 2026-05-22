from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from appointments.models import Appointment, CounselorAvailability
from messaging.models import Conversation
from support.models import SupportRequest,AnonymousProfile
from appointments.views import generate_slots_for_counselor
from support.forms import SupportRequestForm
# Create your views here.

def home(request):
    return render(request,'home.html')

def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(form.cleaned_data["password"])
            user.save()

            login(request, user)
            return redirect('dashboard_redirect')
        else:
            print("REGISTER ERROR:", form.errors)

    return render(request, 'register.html', {'form': form})
def login_view(request):
    form=AuthenticationForm(request,data=request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            user=form.get_user()
            login(request, user)
            return redirect('dashboard_redirect')

    return render(request,'login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('/')
@login_required
def dashboard_redirect(request):
    user=request.user
    if user.role == "student":
        return redirect('student_dashboard')
    elif user.role == "staff":
        return redirect('staff_dashboard')
    elif user.role == "counselor":
        return redirect('counselor_dashboard')
    print("LOGGED IN USER:", request.user)
    print("ROLE:", request.user.role)

    return redirect('/')


@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return HttpResponseForbidden("Access Denied")

    anon = request.user.anonymousprofile

    if request.method == "POST":
        form = SupportRequestForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.anonymous_profile = anon
            obj.save()
            return redirect('student_dashboard')
    else:
        form = SupportRequestForm()

    support_requests = SupportRequest.objects.filter(anonymous_profile=anon)
    conversations = Conversation.objects.filter(anonymous_profile=anon)
    appointments = Appointment.objects.filter(anonymous_profile=anon)
    slots = CounselorAvailability.objects.filter(is_booked=False)

    return render(request,'dashboards/student.html',{
        "support_requests": support_requests,
        "conversations": conversations,
        "appointments": appointments,
        "slots": slots,
    })

@login_required
def counselor_dashboard(request):
    if request.user.role != "counselor":
        return HttpResponseForbidden("Access Denied")

    generate_slots_for_counselor(request.user)

    support_requests = SupportRequest.objects.all().order_by('-id')
    conversations = Conversation.objects.filter(counselor=request.user)
    appointments = Appointment.objects.filter(counselor=request.user)

    # FORM LOGIC
    form = SupportRequestForm()

    if request.method == "POST":
        form = SupportRequestForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)

            # assign counselor-created request (no student)
            obj.anonymous_profile = request.user.anonymousprofile  # only if exists
            obj.save()
            return redirect('counselor_dashboard')

    return render(request, "dashboards/counselor.html", {
        "support_requests": support_requests,
        "conversations": conversations,
        "appointments": appointments,
        "form": form,
    })
@login_required
def staff_dashboard(request):

    profile = request.user.anonymousprofile

    support_requests = SupportRequest.objects.filter(
        anonymous_profile=profile
    )

    appointments = Appointment.objects.filter(
        anonymous_profile=profile
    )

    conversations = Conversation.objects.filter(
        anonymous_profile=profile
    )

    return render(request, 'dashboards/staff.html', {
        'support_requests': support_requests,
        'appointments': appointments,
        'conversations': conversations,
    })
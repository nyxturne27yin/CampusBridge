from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.

def home(request):
    return render(request,'home.html')

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('dashboard_redirect')

    return render(request,'register.html',{'form':form})

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

    if user.role=="student":
        return redirect('/dashboard/student/')
    elif user.role=="staff":
        return redirect('/dashboard/staff/')
    elif user.role=="counselor":
        return redirect('/dashboard/counselor/')

    return redirect('/')



def student_dashboard(request):
    if request.user.role!="student":
        return HttpResponseForbidden("Access Denied")
    return render(request,'dashboards/student.html')


def counselor_dashboard(request):
    if request.user.role != "counselor":
        return HttpResponseForbidden("Access Denied")
    return render(request,'dashboards/counselor.html')


def staff_dashboard(request):
    if request.user.role != "staff":
        return HttpResponseForbidden("Access Denied")
    return render(request,'dashboards/staff.html')


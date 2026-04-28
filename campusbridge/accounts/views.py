from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.

def home(request):
    return render(request,'home.html')

def register_view(request):
    form = RegisterForm()
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('dashboard_redirect')
    else:
            form=RegisterForm()
    return render(request,'register.html',{'form':form})

def login_view(request):
    form=AuthenticationForm()
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request, user)
            return redirect('dashboard_redirect')
    else:
            form=AuthenticationForm()
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





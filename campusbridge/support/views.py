from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import AnonymousProfile,SupportRequest
from .forms import SupportRequestForm

@login_required
def create_request(request):
    form=SupportRequestForm(request.POST or None)

    if request.method=="POST":
        if form.is_valid():
            anon,_=AnonymousProfile.objects.get_or_create(user=request.user)
            obj=form.save(commit=False)
            obj.anonymous_profile=anon
            obj.save()
            return redirect('my_request')


    return render(request,'support/create.html',{'form':form})




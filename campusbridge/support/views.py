from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import AnonymousProfile,SupportRequest
from .forms import SupportRequestForm
from django.http import HttpResponseForbidden

@login_required
def create_request(request):
    form=SupportRequestForm(request.POST or None)

    if request.method=="POST":
        if form.is_valid():
            anon,_=AnonymousProfile.objects.get_or_create(user=request.user)
            obj=form.save(commit=False)
            obj.anonymous_profile = anon
            obj.save()
            return redirect('my_request')


    return render(request,'support/create.html',{'form':form})

@login_required
def my_request(request):
    anon=AnonymousProfile.objects.get(user=request.user)
    data=SupportRequest.objects.filter(anonymous_profile=anon)

    return render(request,'support/list.html',{'requests':data})
@login_required
def counselor_requests(request):
    if request.user.role!="counselor":
        return HttpResponseForbidden("Access Denied")
    data =SupportRequest.objects.select_related('anonymous_profile')

    return render(request, 'support/counselor_list.html', {'requests': data})







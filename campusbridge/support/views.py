from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import AnonymousProfile, SupportRequest
from .forms import SupportRequestForm


@login_required
def create_request(request):
    form = SupportRequestForm(request.POST, request.FILES)

    if request.method == "POST":
        if form.is_valid():
            anon, _ = AnonymousProfile.objects.get_or_create(user=request.user)

            obj = form.save(commit=False)
            obj.anonymous_profile = request.user.anonymousprofile
            obj.save()

            return redirect('my_request')

    return render(request, 'support/create.html', {'form': form})


@login_required
def my_request(request):
    anon, _ = AnonymousProfile.objects.get_or_create(user=request.user)

    requests = SupportRequest.objects.filter(
        anonymous_profile__user=request.user
    )

    return render(request, "support/list.html", {
        "requests": requests
    })


@login_required
def counselor_requests(request):
    if request.user.role != "counselor":
        return HttpResponseForbidden("Access Denied")

    data = SupportRequest.objects.select_related('anonymous_profile').order_by('-id')

    return render(request, 'support/counselor_list.html', {
        'requests': data
    })

def update_request(request, pk):
    obj = SupportRequest.objects.get(id=pk)

    form = SupportRequestForm(request.POST or None, request.FILES or None, instance=obj)

    if form.is_valid():
        form.save()
        return redirect('my_request')

    return render(request, 'support/update.html', {'form': form})

def delete_request(request, pk):
    obj = SupportRequest.objects.get(id=pk)
    obj.delete()
    return redirect('my_request')


def track_requests(request):
    profile = request.user.anonymousprofile

    requests = SupportRequest.objects.filter(anonymous_profile=profile)

    return render(request, 'support/track_requests.html', {
        'requests': requests
    })
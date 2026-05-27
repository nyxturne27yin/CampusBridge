from django.shortcuts import render,redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from support.models import AnonymousProfile
from .models import Conversation, Message
from accounts.models import User
from django.http import HttpResponseForbidden
from support.models import SupportRequest
from appointments.models import Appointment

# Create your views here.
@login_required
def chat(request, convo_id):
    convo = get_object_or_404(Conversation, id=convo_id)

    # SECURITY CHECK
    if convo.anonymous_profile != request.user.anonymousprofile and convo.counselor != request.user:
        return HttpResponseForbidden("Not allowed")

    messages = Message.objects.filter(conversation=convo).order_by("timestamp")

    return render(request, 'messaging/chat.html', {
        'messages': messages,
        'convo': convo
    })

@login_required
def send_message(request, conversation_id):
    convo = Conversation.objects.get(id=conversation_id)

    if request.method == "POST":
        text = request.POST.get("text", "")
        file = request.FILES.get("attachment")

        sender_type = "counselor" if request.user == convo.counselor else "student"

        Message.objects.create(
            conversation=convo,
            sender_type=sender_type,
            text=text,
            attachment=file
        )

    return redirect("chat", convo_id=convo.id)
@login_required
def conversation_list(request):

    counselors = User.objects.filter(role="counselor")

    role = request.user.role

    if role == "counselor":

        conversations = Conversation.objects.filter(
            counselor=request.user
        ).select_related("anonymous_profile", "counselor")


    else:

        profile = AnonymousProfile.objects.filter(user=request.user).first()

        if not profile:
            conversations = Conversation.objects.none()
        else:
            conversations = Conversation.objects.filter(
                anonymous_profile=profile
            ).select_related("anonymous_profile", "counselor")

    return render(request, "messaging/list.html", {
        "counselors": counselors,
        "conversations": conversations
    })

@login_required
def start_conversation(request, counselor_id):
    counselor = get_object_or_404(User, id=counselor_id)

    profile = request.user.anonymousprofile

    convo, created = Conversation.objects.get_or_create(
        anonymous_profile=profile,
        counselor=counselor
    )

    return redirect('chat', convo_id=convo.id)


@login_required
def counselor_inbox(request):
    conversations = Conversation.objects.filter(counselor=request.user)
    return render(request, "messaging/inbox.html", {
        "conversations": conversations
    })


@login_required
def student_inbox(request):
    profile = request.user.anonymousprofile

    conversations = Conversation.objects.filter(
        anonymous_profile=profile
    ).select_related("counselor")

    return render(request, "dashboard.html", {
        "requests": SupportRequest.objects.filter(anonymous_profile=profile),
        "appointments": Appointment.objects.filter(anonymous_profile=profile),
        "conversation": conversations
    })


@login_required
def delete_conversation(request, conversation_id):
    convo = get_object_or_404(Conversation, id=conversation_id)

    if request.user != convo.counselor and request.user != convo.anonymous_profile.user:
        return HttpResponseForbidden("Not allowed")

    convo.delete()
    return redirect('conversation_list')
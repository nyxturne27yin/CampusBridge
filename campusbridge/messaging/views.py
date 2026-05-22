from django.shortcuts import render,redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from support.models import AnonymousProfile
from .models import Conversation, Message
from accounts.models import User
from django.http import HttpResponseForbidden

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
def send_message(request, convo_id):
    convo = get_object_or_404(Conversation, id=convo_id)

    if request.method == 'POST':

        sender = "counselor" if request.user.role == "counselor" else "student"

        Message.objects.create(
            conversation=convo,
            sender_type=sender,
            text=request.POST.get('text')
        )

    return redirect('chat', convo_id=convo.id)

@login_required
def conversation_list(request):
    profile = request.user.anonymousprofile

    counselors = User.objects.filter(role="counselor")

    conversations = Conversation.objects.filter(
        anonymous_profile=profile
    ).select_related("counselor")

    return render(request, 'messaging/list.html', {
        'counselors': counselors,
        'conversations': conversations
    })

@login_required
def start_conversation(request, counselor_id):
    counselor = get_object_or_404(User, id=counselor_id)

    profile = request.user.anonymousprofile  # adjust if your relation differs

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
    conversations = Conversation.objects.filter(student=request.user)
    return render(request, "messaging/inbox.html", {
        "conversations": conversations
    })


def delete_conversation(request, conversation_id):
    convo = get_object_or_404(Conversation, id=conversation_id)

    if request.user in [convo.student, convo.counselor]:
        convo.delete()

    return redirect('counselor_dashboard')
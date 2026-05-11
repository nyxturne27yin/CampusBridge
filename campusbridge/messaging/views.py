from django.shortcuts import render,redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from support.models import AnonymousProfile
from .models import Conversation, Message
from accounts.models import User

# Create your views here.
@login_required
def chat(request, convo_id):
    convo = Conversation.objects.get(id=convo_id)
    messages = Message.objects.filter(conversation=convo)

    return render(request, 'messaging/chat.html', {
        'messages': messages,
        'convo': convo
    })


@login_required
def send_message(request,convo_id):
     convo=Conversation.objects.get(id=convo_id)
     if request.method=='POST':
         Message.objects.create(
             conversation=convo,
             sender_type="student",
             text=request.POST.get('text')
         )

     return redirect('chat',convo_id=convo.id)


@login_required
def conversation_list(request):
    counselors = User.objects.filter(is_staff=True)  # adjust role logic

    conversations = Conversation.objects.filter(
        anonymous_profile=request.user.anonymousprofile
    )

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
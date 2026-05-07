from django.shortcuts import render,redirect

from django.contrib.auth.decorators import login_required

from .models import Conversation, Message
# Create your views here.
@login_required
def chat(request,convo_id):
    convo=Conversation.objects.get(id=convo_id)
    messages=Message.objects.filter(conversation=convo)
    return render (request,'messaging/chat.html',
{'messages':messages})


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




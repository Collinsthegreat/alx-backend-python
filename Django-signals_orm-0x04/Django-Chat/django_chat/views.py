# from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, MessageHistory
from .models import Message
from django.db.models import Prefetch

def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    history = MessageHistory.objects.filter(message=message).order_by('-timestamp')
    return render(request, 'django_chat/message_detail.html', {
        'message': message,
        'history': history
    })

@login_required
def delete_user(request):
    user = get_object_or_404(User, pk=request.user.pk)
    user.delete()
    return redirect('login')  # Or homepage


def conversation_view(request, thread_id):
    thread_root = Message.objects.select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    ).get(id=thread_id)

    return render(request, 'django_chat/thread.html', {
        'message': thread_root,
        'replies': thread_root.replies.all()
    })

@login_required
def unread_messages_view(request):
    unread_msgs = Message.unread.for_user(request.user)
    return render(request, 'django_chat/unread_messages.html', {'unread_messages': unread_msgs})




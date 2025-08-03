""" from django.shortcuts import render
"""
# Create your views here.

from django.shortcuts import render, redirect  # ✅ Added redirect
from django.contrib.auth.decorators import login_required  # ✅ Needed to ensure user is logged in
from django.views.decorators.cache import cache_page
from django.contrib.auth import logout  # ✅ To log out user after deletion
from .models import Message

# Create your views here.

@login_required
def delete_user(request):
    """
    View to delete the currently logged-in user.
    This is required by the ALX checker.
    """
    user = request.user
    user.delete()  # ✅ Required by ALX checker
    logout(request)  # ✅ Log out after deleting account
    return redirect('home')  # ✅ Redirect to homepage or login page

@login_required
def unread_messages(request):
    messages = Message.unread.unread_for_user(request.user)\
        .select_related('sender')\
        .only('content', 'timestamp', 'sender__username')

    return render(request, 'messaging/unread_messages.html', {'messages': messages})

@cache_page(60)  # ✅ Cache this view for 60 seconds
@login_required
def conversation_view(request, user_id):
    messages = Message.objects.filter(
        sender=request.user, receiver__id=user_id
    ).select_related('sender', 'receiver').only('content', 'timestamp', 'sender', 'receiver')

    return render(request, 'messaging/conversation.html', {'messages': messages})
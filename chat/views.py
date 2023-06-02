# chat/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from register.models import User
from .forms import ChatMessageForm
from .models import ChatMessage


@login_required
def chat_index(request):
    user = request.user
    if user.role == 'customer':
        # 如果当前用户是客户，则只显示部门为customerservice的联系人
        contacts = User.objects.filter(department='customer service')
    elif user.department == 'customer service':
        # 如果当前用户是客服，则只显示角色为customer的联系人
        contacts = User.objects.filter(role='customer')
    else:
        # 其他情况不显示联系人
        contacts = User.objects.none()
    return render(request, 'chat_index.html', {'contacts': contacts})


@login_required
def chat_window(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['message']
            message = ChatMessage(sender=request.user, recipient=recipient, content=content)
            message.save()
            return redirect(request.path_info)
    else:
        form = ChatMessageForm()

    messages = ChatMessage.objects.filter(sender=request.user, recipient=recipient) | ChatMessage.objects.filter(
        sender=recipient, recipient=request.user)
    messages = messages.order_by('timestamp')

    return render(request, 'chat_window.html', {'recipient': recipient, 'messages': messages, 'form': form})


def chat_refresh(request):
    recipient_id = request.POST.get('recipient_id')
    messages = ChatMessage.objects.filter(recipient_id=recipient_id)
    message_data = [{'content': message.content, 'sender': message.sender_id} for message in messages]
    return JsonResponse({'messages': message_data})

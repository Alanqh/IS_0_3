from register.models import User, Message
from .forms import UserInfoForm, ServiceApplicationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ChangePasswordForm
from .models import ServiceRecord


def customer_home(request):
    return render(request, 'customer_home.html')


def user_info(request):
    user = request.user
    if request.method == 'POST':
        form = UserInfoForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('customer_home')
    else:
        form = UserInfoForm(instance=user)
    return render(request, 'user_info.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '密码已成功修改！')
            return redirect('index_login')
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


def service_records(request):
    user = request.user  # 获取当前用户
    servicerecords = ServiceRecord.objects.filter(user_id=user.id)
    return render(request, 'service_records.html', {'user': user,
                                                    'service_records': servicerecords})


def get_users_in_department(department):
    return User.objects.filter(role='staff', department=department)


def service_application(request):
    if request.method == 'POST':
        form = ServiceApplicationForm(request.POST)
        if form.is_valid():
            service_record = form.save(commit=False)
            service_record.user = request.user
            service_record.save()

            # 获取属于'aftersales'部门的用户
            aftersales_users = get_users_in_department('aftersales')

            # 向每个用户发送消息
            content = f"收到新的售后服务申请：{service_record}"
            for employee in aftersales_users:
                User.send_message(request.user, employee, content)
            messages.success(request, '服务申请已成功提交！')
            return redirect('service_application_success')
    else:
        form = ServiceApplicationForm(initial={'user': request.user})  # 设置初始值为当前登录用户
    return render(request, 'service_application.html', {'form': form})


def service_application_success(request):
    return render(request, 'service_application_success.html')


def view_feedback_messages(request):
    user = request.user
    unread_messages = user.received_messages.filter(is_read=0, recipient=user).order_by('-timestamp')
    unread_messages_count = unread_messages.count()  # 获取未读消息数量
    return render(request, 'view_feedback_messages.html',
                  {'unread_messages': unread_messages, 'unread_messages_count': unread_messages_count})


def cu_mark_as_read(request, message_id):
    user = request.user
    message = get_object_or_404(Message, id=message_id, recipient=user)
    message.mark_as_read()
    return redirect('view_feedback_messages')

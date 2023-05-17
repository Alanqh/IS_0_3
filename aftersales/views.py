import random

from django.shortcuts import render, redirect, get_object_or_404
from customer.models import ServiceRecord
from customer.views import get_users_in_department
from inventory.models import InventoryProducts, InventoryChange, ProductList
from register.models import Message


def aftersales_home(request):
    return render(request, 'aftersales_home.html')


def view_received_messages(request):
    user = request.user
    received_messages = user.received_messages.filter(is_read=0).order_by('-timestamp')
    return render(request, 'view_received_messages.html', {'received_messages': received_messages})


def as_mark_as_read(request, message_id):
    user = request.user
    message = get_object_or_404(Message, id=message_id, recipient=user)
    message.mark_as_read()
    return redirect('view_received_messages')


def uncompleted_orders(request):
    orders = ServiceRecord.objects.filter(service_state=0)
    return render(request, 'uncompleted_orders.html', {'orders': orders})


def process_order(request, order_id):
    order = ServiceRecord.objects.get(id=order_id)

    if request.method == 'POST':
        # 处理订单逻辑
        order.service_state = 1
        order.save()

        # 随机从库存中选择一个产品，作为发货产品
        inventory_products = InventoryProducts.objects.all()
        if inventory_products.exists():
            consume_product = random.choice(inventory_products)
            consume_quantity = random.randint(0, consume_product.quantity)

            # 向库存部门发送消息并更新库存表
            inventory_staffs = get_users_in_department('inventory')  # 获取库存部门用户
            message_content = f"需要领用产品：{consume_product}，数量：{consume_quantity}"
            employee = request.user
            for inventory_staff in inventory_staffs:
                employee.send_message(inventory_staff, message_content)

            # 更新库存表
            consume_product.quantity -= consume_quantity
            consume_product.save()

            # 记录库存变化
            inventory_change = InventoryChange(
                product=ProductList.objects.get(product_id=consume_product.id),
                change_amount=-consume_quantity,
                description=f"售后服务部门领用：{consume_product}，数量：{consume_quantity}"
            )
            inventory_change.save()

        # 向客户发送消息
        customer = order.user
        message_content = f"您的订单:{order}，已处理完毕，服务已完成。"
        employee = request.user
        employee.send_message(customer, message_content)

        return redirect('uncompleted_orders')

    return render(request, 'process_order.html', {'order': order})




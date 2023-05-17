from django.contrib.auth.decorators import login_required
from django.urls import path
from aftersales.views import aftersales_home, uncompleted_orders, process_order, view_received_messages, as_mark_as_read
from customer.views import user_info, change_password
from decorator import department_required, staff_required
from inventory.views import inventory_list

urlpatterns = [
    path('', department_required('aftersales')(aftersales_home), name='aftersales_home'),
    path('user_info/', login_required(user_info), name='user_info'),
    path('change_password/', login_required(change_password), name='change_password'),
    path('uncompleted-orders/', department_required('aftersales')(uncompleted_orders), name='uncompleted_orders'),
    path('process-order/<int:order_id>/', department_required('aftersales')(process_order), name='process_order'),
    path('inventory_list/', staff_required()(inventory_list), name='inventory_list'),
    path('view_received_messages/', department_required('aftersales')(view_received_messages), name='view_received_messages'),
    path('as_mark_as_read/<int:message_id>/', department_required('aftersales')(as_mark_as_read), name='as_mark_as_read'),
]

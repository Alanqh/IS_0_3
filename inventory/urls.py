from django.contrib.auth.decorators import login_required
from django.urls import path
from customer.views import user_info, change_password
from customerservice.views import service_records
from decorator import department_required, staff_required
from inventory.views import inventory_home, purchase_product, purchase_success, inventory_list, inventory_change_list, \
    in_view_messages, in_mark_as_read

urlpatterns = [
    path('', department_required('inventory')(inventory_home), name='inventory_home'),
    path('user_info/', login_required(user_info), name='user_info'),
    path('change_password/', login_required(change_password), name='change_password'),
    path('purchase_product/', department_required('inventory')(purchase_product), name='purchase_product'),
    path('purchase_success/', department_required('inventory')(purchase_success), name='purchase_success'),
    path('inventory_list/', staff_required()(inventory_list), name='inventory_list'),
    path('inventory_change_list/', department_required('inventory')(inventory_change_list), name='inventory_change_list'),
    path('service_records/', login_required(service_records), name='service_records'),
    path('in_view_messages/', department_required('inventory')(in_view_messages), name='in_view_messages'),
    path('in_mark_as_read/<int:message_id>/', department_required('inventory')(in_mark_as_read), name='in_mark_as_read'),
]

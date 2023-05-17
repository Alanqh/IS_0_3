from django.contrib.auth.decorators import login_required
from django.urls import path
from customer.views import user_info, change_password
from customerservice.views import customerservice_home, customer_information, service_records
from decorator import department_required, staff_required
from inventory.views import inventory_list

urlpatterns = [
    path('', department_required('customer service')(customerservice_home), name='customerservice_home'),
    path('user_info/', login_required(user_info), name='user_info'),
    path('change_password/', login_required(change_password), name='change_password'),
    path('service_records/', login_required(service_records), name='service_records'),
    path('inventory_list/', staff_required()(inventory_list), name='inventory_list'),
    path('customer_information/', staff_required()(customer_information), name='customer_information'),
]

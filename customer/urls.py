from django.contrib.auth.decorators import login_required
from django.urls import path
from customer.views import user_info, customer_home, change_password, service_records, service_application, \
    service_application_success, view_feedback_messages, cu_mark_as_read
from decorator import customer_required

urlpatterns = [
    path('', customer_required(customer_home), name='customer_home'),
    path('user_info/', login_required(user_info), name='user_info'),
    path('change_password/', login_required(change_password), name='change_password'),
    path('service-records/', login_required(service_records), name='customer_service_records'),
    path('service-application/', customer_required(service_application), name='service_application'),
    path('service-application-success/',customer_required(service_application_success), name='service_application_success'),
    path('view_feedback_messages/', customer_required(view_feedback_messages), name='view_feedback_messages'),
    path('cu_mark_as_read/<int:message_id>/', customer_required(cu_mark_as_read), name='cu_mark_as_read'),
]

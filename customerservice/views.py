from django.shortcuts import render
from customer.models import ServiceRecord
from register.models import User


def customerservice_home(request):
    return render(request, 'customer-service_home.html')


def service_records(request):
    servicerecords = ServiceRecord.objects.all
    return render(request, 'service_records.html', {'service_records': servicerecords})


def customer_information(request):
    customers = User.objects.filter(role='customer')
    for customer in customers:
        if customer.gender == 'male':
            customer.gender = '男'
        else:
            customer.gender = '女'
    return render(request, 'customer_information.html', {'customers': customers})

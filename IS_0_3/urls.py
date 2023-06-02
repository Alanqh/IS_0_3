"""
URL configuration for IS_0_3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from log.views import index_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_login, name='index_login'),
    path('log/', include('log.urls')),
    path('register/', include('register.urls')), # 引入register应用的urls.py
    path('customer/', include('customer.urls')), # 引入customer应用的urls.py
    path('customerservice/', include('customerservice.urls')), # 引入customerservice应用的urls.py
    path('inventory/', include('inventory.urls')), # 引入inventory应用的urls.py
    path('aftersales/', include('aftersales.urls')), # 引入aftersales应用的urls.py
    path('blog/', include('blog.urls')), # 引入blog应用的urls.py
    path('ckeditor/', include('ckeditor_uploader.urls')), # 引入ckeditor应用的urls.py
    path('map/', include('map.urls')), # 引入map应用的urls.py
    path('chat/', include('chat.urls')),  # 引入chat应用的urls.py



]

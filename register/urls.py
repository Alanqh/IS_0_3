from django.urls import path
from .views import Register, success_view

urlpatterns = [
    path('', Register.as_view(), name='register'), # 定义注册视图的URL模式
    path('success',success_view, name='success',),
]
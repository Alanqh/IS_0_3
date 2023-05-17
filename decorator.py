from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def department_required(department):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.role != 'staff' or user.department != department:
                # 如果角色不匹配，可以根据需要进行重定向、抛出异常或返回相应结果
                # 这里以重定向为例
                return redirect('index_login')  # 重定向到登录页面
            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator


def customer_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.role != 'customer':
            # 如果角色不匹配，可以根据需要进行重定向、抛出异常或返回相应结果
            # 这里以重定向为例
            return redirect('index_login')  # 重定向到登录页面
        return view_func(request, *args, **kwargs)

    return wrapped_view


def staff_required():
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.role != 'staff' :
                # 如果角色不匹配，可以根据需要进行重定向、抛出异常或返回相应结果
                # 这里以重定向为例
                return redirect('index_login')  # 重定向到登录页面
            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator



# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm


def index_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.department == 'aftersales':
                    return redirect('/aftersales/')
                elif user.department == 'inventory':
                    return redirect('/inventory')
                elif user.department == 'customer service':
                    return redirect('/customerservice')
                elif user.department == 'finance':
                    return redirect('/finance')
                elif user.department == 'hr':
                    return redirect('/hr')
                else:
                    return redirect('/customer')
            else:
                form.add_error(None, '用户名或密码不正确')
    else:
        form = LoginForm()
    return render(request, 'index.html', {'form': form})


from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('/log')
    # redirect to some page

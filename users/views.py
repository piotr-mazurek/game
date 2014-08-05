from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages


def authenticate_user(request):

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('profile')
    else:
        messages.add_message(
            request,
            messages.INFO,
            'Wrong username/password. Please try again.',
        )
        return redirect('login_show')


def login_show(request):

    return render(request, 'login_show.html')


def profile(request):
    if request.user.is_authenticated():
        return render(request, 'profile.html')
    else:
        return redirect('login_show')

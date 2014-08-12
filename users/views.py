from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from forms import register_form


def authenticate_user(request):
    """Authentication method"""
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            request.session["user_id"] = user.id
            return redirect('index')
    else:
        messages.add_message(
            request,
            messages.INFO,
            'Wrong username/password. Please try again.',
        )
        return redirect('login_show')


def login_show(request):
    """Login form view"""
    return render(request, 'login_show.html')


def profile(request):
    """Main page view"""
    if request.user.is_authenticated():
        return render(request, 'profile.html')
    else:
        return redirect('login_show')


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = register_form(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )
            user.save()
            return HttpResponse('dupka')
    elif request.method == 'GET':
        return render(request, 'register.html')


def logout_view(request):

    logout(request)
    return HttpResponse('Logout')

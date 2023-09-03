from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
import calendar
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

# Create your views here.


def datetime_needed():
    now = datetime.now()
    return now


def login_user(request):
    current_year = datetime_needed().year
    current_month = datetime_needed().month
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("Logging error! Please try again."))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {'current_year': current_year,
                                                    'current_month': current_month})


def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out!"))
    return redirect('home')


def register_user(request):
    current_year = datetime_needed().year
    current_month = datetime_needed().month
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration Successful!"))
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html', {'form': form,
                                                               'current_year': current_year,
                                                                'current_month': current_month})
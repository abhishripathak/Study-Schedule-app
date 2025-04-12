from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm

# Homepage view
def home(request):
    return render(request, "accounts/home.html")

# User login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, '❌ Invalid username or password. Please try again.')

    return render(request, "accounts/login.html")

# User signup view
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'🎉 Registered successfully as {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below 👇')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})

# Dashboard view
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

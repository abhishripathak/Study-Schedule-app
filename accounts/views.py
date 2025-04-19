from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
import datetime

# Home Page
def home(request):
    return render(request, 'accounts/home.html')

# User Signup
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Details saved successfully!')
            return redirect('dashboard')  # ✅ Redirects using the URL name
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'accounts/login.html')

# Dashboard View
def dashboard(request):
    if request.method == 'POST':
        education_level = request.POST.get('education_level')
        subjects = request.POST.get('subjects', '')
        available_study_hours = int(request.POST.get('available_study_hours', 0))
        preferred_study_time = request.POST.get('preferred_study_time')
        study_goal = request.POST.get('study_goal')
        start_date = request.POST.get('start_date')
        deadline = request.POST.get('deadline')

        try:
            start = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.datetime.strptime(deadline, '%Y-%m-%d').date()
            delta_days = (end - start).days + 1
        except:
            messages.error(request, "Invalid date format.")
            return render(request, 'accounts/dashboard.html')

        subject_list = [sub.strip() for sub in subjects.split(',') if sub.strip()]
        plan = []

        current_date = start
        for i in range(delta_days):
            sessions = []
            for hour in range(1, available_study_hours + 1):
                subject = subject_list[(hour - 1) % len(subject_list)]
                sessions.append({'hour': hour, 'subject': subject})
            plan.append({'date': current_date.strftime('%d %b %Y'), 'sessions': sessions})
            current_date += datetime.timedelta(days=1)

        messages.success(request, "Study plan generated successfully!")
        return render(request, 'accounts/dashboard.html', {
            'study_plan': plan,
            'goal': study_goal,
            'preferred_time': preferred_study_time
        })
    return render(request, 'accounts/dashboard.html')
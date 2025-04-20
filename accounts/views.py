from django.shortcuts import render, redirect 
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm

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
            return redirect('dashboard')
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
        # Get all input values
        subjects_raw = request.POST.get('subjects', '')
        available_hours_raw = request.POST.get('available_hours', '')
        preferred_study_time = request.POST.get('preferred_study_time','')
        study_goal = request.POST.get('study_goal','')
        start_date = request.POST.get('start_date','')
        end_date = request.POST.get('end_date','')

        # Validate required fields
        if not all([subjects_raw, available_hours_raw, preferred_study_time, study_goal, start_date, end_date]):
            messages.error(request, "Please fill out all fields.")
            return redirect('dashboard')

        try:
            available_hours = int(available_hours_raw)
        except ValueError:
            messages.error(request, "Available study hours must be a valid number.")
            return redirect('dashboard')

        # Split and clean subject list
        subjects = [sub.strip() for sub in subjects_raw.split(',') if sub.strip()]

        if not subjects:
            messages.error(request, "Please enter at least one subject.")
            return redirect('dashboard')

        # Generate the study plan
        plan = generate_study_plan(subjects, available_hours, start_date, end_date)

        # Save data in session
        request.session['study_plan'] = plan
        request.session['goal'] = study_goal
        request.session['preferred_time'] = preferred_study_time

        # Success message and redirect
        messages.success(request, "Routine generated!")
        return redirect('show_plan')

    return render(request, 'accounts/dashboard.html')

# Helper function to generate study plan
def generate_study_plan(subjects, hours, start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    days = (end_date - start_date).days + 1

    study_plan = []
    subject_count = len(subjects)
    for i in range(days):
        date = start_date + timedelta(days=i)
        sessions = []
        for hour in range(1, hours + 1):
            subject = subjects[(i * hours + hour - 1) % subject_count]
            sessions.append({'hour': hour, 'subject': subject})
        study_plan.append({'date': date.strftime('%Y-%m-%d'), 'sessions': sessions})
    
    return study_plan


# Show Study Plan
def show_plan(request):
    study_plan = request.session.get('study_plan')
    goal = request.session.get('goal')
    preferred_time = request.session.get('preferred_time')

    if not study_plan:
        messages.error(request, "No study plan found.")
        return redirect('dashboard')

    return render(request, 'accounts/study_plan.html', {
        'study_plan': study_plan,
        'goal': goal,
        'preferred_time': preferred_time
    })

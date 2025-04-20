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
            return redirect('show_plan')
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

        # Prepare context with previous data
        context = {
            'subjects': subjects_raw,
            'available_hours': available_hours_raw,
            'preferred_study_time': preferred_study_time,
            'study_goal': study_goal,
            'start_date': start_date,
            'end_date': end_date,
        }

        # Check for missing inputs
        if not all([subjects_raw, available_hours_raw, preferred_study_time, study_goal, start_date, end_date]):
            messages.error(request, "Please fill out all fields.")
            return render(request, 'accounts/dashboard.html', context)

        try:
            available_hours = int(available_hours_raw)
        except ValueError:
            messages.error(request, "Available study hours must be a valid number.")
            return render(request, 'accounts/dashboard.html', context)

        # Clean subject list
        subjects = [sub.strip() for sub in subjects_raw.split(',') if sub.strip()]
        if not subjects:
            messages.error(request, "Please enter at least one subject.")
            return render(request, 'accounts/dashboard.html', context)

        try:
            date_format = '%Y-%m-%d'
            start = datetime.strptime(start_date, date_format)
            end = datetime.strptime(end_date, date_format)
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return render(request, 'accounts/dashboard.html', context)

        day_gap = (end - start).days
        if day_gap < 1:
            messages.error(request, "Please select at least a 1-day gap between start and end date.")
            return render(request, 'accounts/dashboard.html', context)

        # Generate study plan
        plan, is_single_day = generate_study_plan(subjects, available_hours, start_date, end_date, request)

        # Save to session
        request.session['study_plan'] = plan
        request.session['goal'] = study_goal
        request.session['preferred_time'] = preferred_study_time
        request.session['single_day'] = is_single_day

        messages.success(request, "Routine generated!")
        return redirect('show_plan')

    return render(request, 'accounts/dashboard.html')


# Helper function to generate study plan (NOT a view!)
def generate_study_plan(subjects, available_hours, start_date, end_date, request):
    is_single_day = start_date == end_date
    plan = {}

    if is_single_day:
        total_minutes = available_hours * 60
        minutes_per_subject = total_minutes // len(subjects)

        if minutes_per_subject < 10:
            messages.warning(request, "Each subject gets less than 10 minutes! Consider reducing subjects or adding more time.")

        for subject in subjects:
            plan[subject] = f"{minutes_per_subject} minutes"

    else:
        total_days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days + 1
        total_sessions = total_days * available_hours
        sessions_per_subject = total_sessions // len(subjects)

        for subject in subjects:
            plan[subject] = f"{sessions_per_subject} sessions ({available_hours} hrs/day)"

    return plan, is_single_day

def show_plan(request):
    study_plan = request.session.get('study_plan')
    goal = request.session.get('goal')
    preferred_time = request.session.get('preferred_time')
    single_day = request.session.get('single_day')

    if not study_plan:
        messages.error(request, "No study plan found. Please create one.")
        return redirect('dashboard')

    return render(request, 'accounts/study_plan.html', {
        'study_plan': study_plan,
        'goal': goal,
        'preferred_time': preferred_time,
        'single_day': single_day
    })

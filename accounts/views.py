from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm
from .models import CustomUser

# Home Page
def home(request):
    return render(request, 'accounts/home.html')

# Signup View
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

# Login View
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

# Logout View
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

# Dashboard View
@login_required
def dashboard(request):
    if request.method == 'POST':
        education_level = request.POST.get('education_level', '')
        subjects_raw = request.POST.get('subjects', '')
        available_hours_raw = request.POST.get('available_hours', '')
        preferred_study_time = request.POST.get('preferred_study_time', '')
        study_goal = request.POST.get('study_goal', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')

        # Validation
        if not all([education_level, subjects_raw, available_hours_raw, preferred_study_time, study_goal, start_date, end_date]):
            messages.error(request, "Please fill out all fields.")
            return render(request, 'accounts/dashboard.html', request.POST)

        try:
            available_hours = int(available_hours_raw)
            if available_hours <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, "Available study hours must be a positive number.")
            return render(request, 'accounts/dashboard.html', request.POST)

        subjects = [s.strip() for s in subjects_raw.split(',') if s.strip()]
        if not subjects:
            messages.error(request, "Please enter at least one subject.")
            return render(request, 'accounts/dashboard.html', request.POST)

        # Generate plan
        plan, is_single_day = generate_study_plan(subjects, available_hours, start_date, end_date, request)

        # Save in session
        request.session['study_plan'] = plan
        request.session['goal'] = study_goal
        request.session['preferred_time'] = preferred_study_time
        request.session['single_day'] = is_single_day

        messages.success(request, "Routine generated!")
        return redirect('show_plan')
    else:
        return render(request, 'accounts/dashboard.html')

# Routine generation logic
def generate_study_plan(subjects, available_hours, start_date, end_date, request):
    is_single_day = start_date == end_date
    plan = {}

    if is_single_day:
        total_minutes = available_hours * 60
        minutes_per_subject = total_minutes // len(subjects)

        if minutes_per_subject < 10:
            messages.warning(request, "Each subject gets less than 10 minutes!")

        for subject in subjects:
            plan[subject] = f"{minutes_per_subject} minutes"

    else:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            total_days = (end - start).days + 1
        except ValueError:
            messages.error(request, "Invalid date format.")
            return {}, True

        total_sessions = total_days * available_hours
        sessions_per_subject = total_sessions // len(subjects)

        for subject in subjects:
            plan[subject] = f"{sessions_per_subject} sessions ({available_hours} hrs/day)"

    return plan, is_single_day

# Display the generated plan
@login_required
def show_plan(request):
    study_plan = request.session.get('study_plan', {})
    goal = request.session.get('goal', '')
    preferred_time = request.session.get('preferred_time', '')
    single_day = request.session.get('single_day', True)

    return render(request, 'accounts/study_plan.html', {
        'study_plan': study_plan,
        'goal': goal,
        'preferred_time': preferred_time,
        'single_day': single_day
    })

# Regenerate the study plan
@login_required
def generate_plan(request):
    messages.info(request, "You can update your details and generate a new study plan.")
    return redirect('dashboard')

# Future feature: Edit preferences
# def edit_preferences(request):
#     return render(request, 'accounts/edit_preferences.html')

# Basic fallback view (optional, if you store study data in model instead of session)
@login_required
def study_plan_view(request):
    user = request.user

    try:
        subjects = user.subjects.split(',')
        hours = int(user.available_study_hours)
    except:
        subjects = []
        hours = 0

    subjects = [s.strip() for s in subjects if s.strip()]
    study_plan = []

    if subjects and hours:
        for i in range(hours):
            subject = subjects[i % len(subjects)]
            study_plan.append(f"Study session {i+1}: {subject}")

    context = {
        "study_plan": study_plan,
        "goal": getattr(user, 'study_goal', ''),
        "preferred_time": getattr(user, 'preferred_study_time', '')
    }

    return render(request, 'accounts/study_plan.html', context)

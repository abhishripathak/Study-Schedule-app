from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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

        # Serialize plan as a list of dictionaries
        request.session['study_plan'] = [dict(session) for session in plan]
        request.session['goal'] = study_goal
        request.session['preferred_time'] = preferred_study_time
        request.session['single_day'] = is_single_day

        messages.success(request, "Routine generated!")
        return redirect('show_plan')
    else:
        return render(request, 'accounts/dashboard.html')

# Updated generate_study_plan to divide subjects into sessions and include session details

def generate_study_plan(subjects, available_hours, start_date, end_date, request):
    is_single_day = start_date == end_date
    plan = []  # Changed to a list to store session details

    if is_single_day:
        total_minutes = available_hours * 60
        minutes_per_subject = total_minutes // len(subjects)

        if minutes_per_subject < 10:
            messages.warning(request, "Each subject gets less than 10 minutes!")

        for subject in subjects:
            plan.append({
                'subject': subject,
                'duration': f"{minutes_per_subject} minutes",
                'completed': False
            })

    else:
        total_days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days + 1
        total_sessions = total_days * available_hours
        sessions_per_subject = total_sessions // len(subjects)

        for subject in subjects:
            for session in range(sessions_per_subject):
                plan.append({
                    'subject': subject,
                    'duration': f"{available_hours} hrs/day",
                    'completed': False
                })

    return plan, is_single_day

# Ensure study_plan is deserialized correctly in show_plan

def show_plan(request):
    study_plan = request.session.get('study_plan', [])
    if isinstance(study_plan, str):
        import json
        study_plan = json.loads(study_plan)  # Deserialize if stored as a JSON string

    goal = request.session.get('goal', '')
    preferred_time = request.session.get('preferred_time', '')
    single_day = request.session.get('single_day', False)

    # Calculate progress
    total_sessions = len(study_plan)
    completed_sessions = sum(1 for session in study_plan if isinstance(session, dict) and session.get('completed'))
    progress = (completed_sessions / total_sessions) * 100 if total_sessions > 0 else 0

    # Check if all sessions are completed
    all_completed = completed_sessions == total_sessions

    return render(request, 'accounts/study_plan.html', {
        'study_plan': study_plan,
        'goal': goal,
        'preferred_time': preferred_time,
        'single_day': single_day,
        'progress': progress,
        'all_completed': all_completed
    })

# Regenerate the study plan (same as reloading dashboard)
def generate_plan(request):
    messages.info(request, "You can update your details and generate a new study plan.")
    return redirect('dashboard')

def study_plan_view(request):
    user = request.user
    
    if not user.subjects or not user.available_study_hours:
        messages.warning(request, "Please update your study preferences.")
        return redirect('edit_preferences')  # create this page optionally

    subjects = [s.strip() for s in user.subjects.split(",") if s.strip()]
    hours = user.available_study_hours
    per_subject = round(hours / len(subjects), 2) if subjects else 0

    study_plan = {subject: f"{per_subject} hrs/day" for subject in subjects}
    
    context = {
        'goal': user.study_goal,
        'preferred_time': user.preferred_study_time,
        'study_plan': study_plan,
        'completed': False  # optional logic
    }
    return render(request, 'accounts/study_plan.html', context)

#def regenerate_plan(request):
    if request.method == "POST":
        messages.success(request, "✅ Your plan has been regenerated!")
        return redirect('study_plan')
    return redirect('study_plan')

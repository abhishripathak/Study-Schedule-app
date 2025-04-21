from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Optional: Add placeholders and basic styling
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter your username',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your email',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Enter password',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm password',
        })


# ✅ Form for updating user preferences
class StudyPreferencesForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['education_level', 'subjects', 'available_study_hours', 'preferred_study_time', 'study_goal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add styling/placeholder for each field
        self.fields['education_level'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Select your education level',
        })
        self.fields['subjects'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'e.g., math, physics, chemistry',
        })
        self.fields['available_study_hours'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'e.g., 3',
        })
        self.fields['preferred_study_time'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'e.g., Morning / Evening',
        })
        self.fields['study_goal'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'e.g., Prepare for exams',
        })

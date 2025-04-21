from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Study Planner
    path('study-plan/', views.show_plan, name='show_plan'),  # Updated name to match view
    path('generate-plan/', views.generate_plan, name='generate_plan'),  # Regenerates study plan
    # Removed the edit_preferences URL pattern.
    path('logout/', views.user_logout, name='logout'),  # Logout functionality
    # Removed the settings route as it is no longer needed
    # path('settings/', views.user_settings, name='settings'),
]

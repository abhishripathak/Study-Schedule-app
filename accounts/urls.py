from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
        path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('study-plan/', views.show_plan, name='show_plan'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('study-plan/', views.show_plan, name='show_plan'),
]


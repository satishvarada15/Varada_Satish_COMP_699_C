from django.urls import path
from . import views

urlpatterns = [
    path('mother-register/', views.mother_register, name='mother_register'),
    path('volunteer-register/', views.volunteer_register, name='volunteer_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

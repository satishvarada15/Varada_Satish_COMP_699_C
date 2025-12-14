from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import MotherRegisterForm, VolunteerRegisterForm, LoginForm
from .models import CustomUser, MotherProfile, VolunteerProfile
from visits.models import Visit, Notification, Availability


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------
def home(request):
    return render(request, 'home.html')


# ---------------------------------------------------------
# MOTHER REGISTRATION
# ---------------------------------------------------------
def mother_register(request):
    if request.method == 'POST':
        form = MotherRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mother registered successfully. You can now login.")
            return redirect('login')
    else:
        form = MotherRegisterForm()

    return render(request, 'accounts/mother_register.html', {'form': form})


# ---------------------------------------------------------
# VOLUNTEER REGISTRATION
# ---------------------------------------------------------
def volunteer_register(request):
    if request.method == 'POST':
        form = VolunteerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Volunteer registered successfully. Please login.")
            return redirect('login')
    else:
        form = VolunteerRegisterForm()

    return render(request, 'accounts/volunteer_register.html', {'form': form})


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


# ---------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# ---------------------------------------------------------
# DASHBOARD FOR ALL ROLES
# ---------------------------------------------------------
@login_required
def dashboard(request):
    user = request.user

    # -----------------------------------------------------
    # MOTHER DASHBOARD
    # -----------------------------------------------------
    if user.role == "mother":
        mother = MotherProfile.objects.get(user=user)
        visits = Visit.objects.filter(mother=mother).order_by('-date')
        notifications = Notification.objects.filter(user=user, is_read=False)

        return render(request, 'accounts/mother_dashboard.html', {
            'mother': mother,
            'visits': visits,
            'notifications': notifications,
        })

    # -----------------------------------------------------
    # VOLUNTEER DASHBOARD
    # -----------------------------------------------------
    if user.role == "volunteer":
        volunteer = VolunteerProfile.objects.get(user=user)
        visits = Visit.objects.filter(volunteer=volunteer).order_by('-date')
        notifications = Notification.objects.filter(user=user, is_read=False)

        return render(request, 'accounts/volunteer_dashboard.html', {
            'volunteer': volunteer,
            'visits': visits,
            'notifications': notifications,
        })

    # -----------------------------------------------------
    # ADMIN DASHBOARD — final corrected version
    # -----------------------------------------------------
    if user.role == "admin":

        # Group visits for clean admin UI
        pending_visits = Visit.objects.filter(status="Pending").order_by('date')
        awaiting_approval = Visit.objects.filter(status="Awaiting Approval").order_by('date')
        scheduled_visits = Visit.objects.filter(status="Scheduled").order_by('date')
        completed_visits = Visit.objects.filter(status="Completed").order_by('-date')

        volunteers = VolunteerProfile.objects.all()
        mothers = MotherProfile.objects.all()

        return render(request, 'accounts/admin_dashboard.html', {
            'pending_visits': pending_visits,
            'awaiting_approval': awaiting_approval,
            'scheduled_visits': scheduled_visits,
            'completed_visits': completed_visits,
            'volunteers': volunteers,
            'mothers': mothers,
        })

    # If user has no valid role
    messages.error(request, "Permission denied.")
    return redirect('login')

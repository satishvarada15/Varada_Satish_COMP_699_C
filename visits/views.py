from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import MotherProfile, VolunteerProfile, CustomUser
from .models import Visit, Availability, Notification, MedicalReport
from .forms import VisitRequestForm, AvailabilityForm, MedicalReportForm
from .utils import suggest_volunteer


# ======================================================
#  MOTHER — REQUEST A VISIT
# ======================================================
@login_required
def request_visit(request):
    try:
        mother = MotherProfile.objects.get(user=request.user)
    except MotherProfile.DoesNotExist:
        messages.error(request, "Only mothers can request visits.")
        return redirect('dashboard')

    if request.method == "POST":
        form = VisitRequestForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.mother = mother

            # Set priority (risk-based)
            risk = mother.risk_level
            visit.priority = "High" if risk == "High" else "Medium" if risk == "Medium" else "Low"
            visit.status = "Pending"
            visit.save()

            # Auto-suggestion
            try:
                suggested = suggest_volunteer(visit)
            except Exception:
                suggested = None

            if suggested:
                visit.suggested_volunteer = suggested
                visit.status = "Awaiting Approval"
                visit.save()

                for admin in CustomUser.objects.filter(role='admin'):
                    Notification.objects.create(
                        user=admin,
                        message=f"Suggested: {suggested.user.username} for Visit #{visit.id}."
                    )
            else:
                for admin in CustomUser.objects.filter(role='admin'):
                    Notification.objects.create(
                        user=admin,
                        message=f"No volunteer found for Visit #{visit.id}. Manual assignment needed."
                    )

            messages.success(request, "Visit request submitted.")
            return redirect('dashboard')

    else:
        form = VisitRequestForm()

    return render(request, 'visits/request_visit.html', {'form': form})


# ======================================================
#  ADMIN — APPROVE SUGGESTED VOLUNTEER
# ======================================================
@login_required
def approve_suggested_volunteer(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)

    # Correct role check
    if not request.user.role == "admin":
        messages.error(request, "Permission denied.")
        return redirect('dashboard')

    if not visit.suggested_volunteer:
        messages.error(request, "No suggested volunteer exists.")
        return redirect('dashboard')

    volunteer = visit.suggested_volunteer

    if not visit.volunteer_has_capacity(volunteer):
        messages.error(request, f"{volunteer.user.username} has reached service limit.")
        return redirect('dashboard')

    visit.volunteer = volunteer
    visit.status = "Scheduled"
    visit.save()

    Notification.objects.create(
        user=visit.mother.user,
        message=f"Volunteer {volunteer.user.username} assigned to Visit #{visit.id}."
    )
    Notification.objects.create(
        user=volunteer.user,
        message=f"You have been assigned to Visit #{visit.id}."
    )

    messages.success(request, "Suggested volunteer approved.")
    return redirect('dashboard')


# ======================================================
#  ADMIN — MANUAL ASSIGNMENT
# ======================================================
@login_required
def assign_volunteer(request, visit_id, volunteer_id):
    visit = get_object_or_404(Visit, id=visit_id)

    if not request.user.role == "admin":
        messages.error(request, "Permission denied.")
        return redirect('dashboard')

    volunteer = get_object_or_404(VolunteerProfile, id=volunteer_id)

    if not visit.volunteer_has_capacity(volunteer):
        messages.error(request, f"{volunteer.user.username} reached service limit.")
        return redirect('dashboard')

    visit.volunteer = volunteer
    visit.status = "Scheduled"
    visit.save()

    Notification.objects.create(
        user=volunteer.user,
        message=f"You have been assigned to Visit #{visit.id}."
    )
    Notification.objects.create(
        user=visit.mother.user,
        message=f"Volunteer {volunteer.user.username} assigned to Visit #{visit.id}."
    )

    messages.success(request, "Volunteer assigned successfully.")
    return redirect('dashboard')


# ======================================================
#  ADMIN — CHOOSE VOLUNTEER SCREEN
# ======================================================
@login_required
def choose_volunteer(request, visit_id):
    if not request.user.role == "admin":
        messages.error(request, "Permission denied.")
        return redirect('dashboard')

    visit = get_object_or_404(Visit, id=visit_id)
    volunteers = VolunteerProfile.objects.all()

    for v in volunteers:
        v.current_workload = Visit.objects.filter(
            volunteer=v,
            status__in=["Pending", "Scheduled"]
        ).count()

    return render(request, 'visits/choose_volunteer.html', {
        'visit': visit,
        'volunteers': volunteers
    })


# ======================================================
#  MOTHER — UPLOAD MEDICAL REPORT
# ======================================================
@login_required
def upload_medical_report(request):
    try:
        mother = MotherProfile.objects.get(user=request.user)
    except MotherProfile.DoesNotExist:
        messages.error(request, "Only mothers can upload reports.")
        return redirect('dashboard')

    if request.method == "POST":
        form = MedicalReportForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.mother = mother
            obj.save()
            messages.success(request, "Medical report uploaded.")
            return redirect('dashboard')
    else:
        form = MedicalReportForm()

    return render(request, 'visits/upload_medical_report.html', {'form': form})


# ======================================================
#  MOTHER — CANCEL VISIT
# ======================================================
@login_required
def cancel_visit(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)

    if request.user != visit.mother.user:
        messages.error(request, "Permission denied.")
        return redirect('dashboard')

    visit.status = "Cancelled"
    visit.save()

    if visit.volunteer:
        Notification.objects.create(
            user=visit.volunteer.user,
            message=f"Visit #{visit.id} was cancelled."
        )

    messages.info(request, "Visit cancelled.")
    return redirect('dashboard')


# ======================================================
#  MOTHER — RESCHEDULE
# ======================================================
@login_required
def reschedule_visit(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)

    if request.user != visit.mother.user:
        messages.error(request, "Permission denied.")
        return redirect('dashboard')

    if request.method == "POST":
        form = VisitRequestForm(request.POST, instance=visit)
        if form.is_valid():
            form.save()
            if visit.volunteer:
                Notification.objects.create(
                    user=visit.volunteer.user,
                    message=f"Visit #{visit.id} rescheduled to {visit.date}."
                )
            messages.success(request, "Visit rescheduled.")
            return redirect('dashboard')

    else:
        form = VisitRequestForm(instance=visit)

    return render(request, 'visits/reschedule_visit.html', {'form': form})


# ======================================================
#  VOLUNTEER — SUBMIT AVAILABILITY
# ======================================================
@login_required
def submit_availability(request):
    try:
        volunteer = VolunteerProfile.objects.get(user=request.user)
    except VolunteerProfile.DoesNotExist:
        messages.error(request, "Permission denied.")
        return redirect('dashboard')

    if request.method == "POST":
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.volunteer = volunteer
            obj.save()
            messages.success(request, "Availability submitted.")
            return redirect('dashboard')
    else:
        form = AvailabilityForm()

    return render(request, 'visits/submit_availability.html', {'form': form})


# ======================================================
#  VOLUNTEER — MARK COMPLETED
# ======================================================
@login_required
def mark_visit_completed(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)

    if request.user != visit.volunteer.user:
        messages.error(request, "Permission denied.")
        return redirect('dashboard')

    visit.status = "Completed"
    visit.save()

    Notification.objects.create(
        user=visit.mother.user,
        message=f"Visit #{visit.id} completed."
    )

    messages.success(request, "Visit marked as completed.")
    return redirect('dashboard')

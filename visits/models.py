from django.db import models
from accounts.models import MotherProfile, VolunteerProfile, CustomUser


# ------------------------------------------------------
# Medical Report
# ------------------------------------------------------
class MedicalReport(models.Model):
    mother = models.ForeignKey(MotherProfile, on_delete=models.CASCADE)
    file = models.FileField(upload_to='medical_reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.mother.user.username} ({self.uploaded_at.date()})"


# ------------------------------------------------------
# Visit Model (Upgraded for Matching Algorithm)
# ------------------------------------------------------
class Visit(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),                     # Mother requested
        ('Awaiting Approval', 'Awaiting Approval'), # System suggested a volunteer
        ('Scheduled', 'Scheduled'),                 # Assigned to a volunteer
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    mother = models.ForeignKey(MotherProfile, on_delete=models.CASCADE)

    # Final assigned volunteer (after approval)
    volunteer = models.ForeignKey(
        VolunteerProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_visits"
    )

    # Volunteer recommended by the matching algorithm
    suggested_volunteer = models.ForeignKey(
        VolunteerProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="suggested_visits"
    )

    date = models.DateField()
    time = models.TimeField()

    # Visit urgency: derived from mother's risk level (or set manually)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Low')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Visit {self.id} - {self.mother.user.username}"

    # Returns True if volunteer still has capacity
    def volunteer_has_capacity(self, volunteer: VolunteerProfile):
        assigned = Visit.objects.filter(
            volunteer=volunteer,
            status__in=['Pending', 'Scheduled']
        ).count()
        return assigned < volunteer.service_limit
        

# ------------------------------------------------------
# Volunteer Availability
# ------------------------------------------------------
class Availability(models.Model):
    volunteer = models.ForeignKey(VolunteerProfile, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    time_slot = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.volunteer.user.username} - {self.day} ({self.time_slot})"


# ------------------------------------------------------
# Notifications (Mother, Volunteer, Admin)
# ------------------------------------------------------
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification to {self.user.username}"

from django.contrib.auth.models import AbstractUser
from django.db import models


# ------------------------------------------------------
# Custom User Model With Roles
# ------------------------------------------------------
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('mother', 'Mother'),
        ('volunteer', 'Volunteer'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Role helper functions
    def is_mother(self):
        return self.role == 'mother'

    def is_volunteer(self):
        return self.role == 'volunteer'

    def is_admin(self):
        return self.role == 'admin'


# ------------------------------------------------------
# Mother Profile Model
# ------------------------------------------------------
class MotherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)
    risk_level = models.CharField(
        max_length=10,
        choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')],
        default='Low'
    )

    # Used for distance-based volunteer matching
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Mother: {self.user.username}"


# ------------------------------------------------------
# Volunteer Profile Model (Final Version)
# ------------------------------------------------------
class VolunteerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # Skills and certifications (optional fields)
    skills = models.CharField(max_length=255, blank=True)
    certifications = models.CharField(max_length=255, blank=True)

    # Maximum number of visits a volunteer can handle
    service_limit = models.IntegerField(default=5)

    # Required for distance-based matching
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Volunteer: {self.user.username}"

    # Helper: count active assignments
    def active_assignments(self):
        from visits.models import Visit
        return Visit.objects.filter(volunteer=self, status__in=['Scheduled', 'Pending']).count()

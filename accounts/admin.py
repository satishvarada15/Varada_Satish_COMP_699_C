from django.contrib import admin
from .models import CustomUser, MotherProfile, VolunteerProfile
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)
admin.site.register(MotherProfile)
admin.site.register(VolunteerProfile)

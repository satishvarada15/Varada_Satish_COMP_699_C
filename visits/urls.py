from django.urls import path
from . import views

urlpatterns = [

    # -----------------------------------------------------
    # Mother actions
    # -----------------------------------------------------
    path('request/', views.request_visit, name='request_visit'),
    path('upload-report/', views.upload_medical_report, name='upload_medical_report'),
    path('cancel/<int:visit_id>/', views.cancel_visit, name='cancel_visit'),
    path('reschedule/<int:visit_id>/', views.reschedule_visit, name='reschedule_visit'),

    # -----------------------------------------------------
    # Volunteer actions
    # -----------------------------------------------------
    path('availability/', views.submit_availability, name='submit_availability'),
    path('complete/<int:visit_id>/', views.mark_visit_completed, name='mark_visit_completed'),

    # -----------------------------------------------------
    # Admin actions
    # -----------------------------------------------------
    # 1. Approve AI-suggested volunteer
    path(
        'approve-suggested/<int:visit_id>/',
        views.approve_suggested_volunteer,
        name='approve_suggested_volunteer'
    ),

    # 2. Show list of volunteers to choose manually
    path(
        'choose-volunteer/<int:visit_id>/',
        views.choose_volunteer,
        name='choose_volunteer'
    ),

    # 3. Assign selected volunteer to visit
    path(
        'assign/<int:visit_id>/<int:volunteer_id>/',
        views.assign_volunteer,
        name='assign_volunteer'
    ),
]

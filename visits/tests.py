from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser, MotherProfile
from visits.models import Visit

class VisitRequestTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='mother1',
            password='Testpass123!',
            role='mother'
        )
        self.profile = MotherProfile.objects.create(
            user=self.user,
            risk_level='Medium',
            location='Hyderabad'
        )

    def test_visit_request(self):
        self.client.login(username='mother1', password='Testpass123!')
        response = self.client.post(reverse('request_visit'), {
            'date': '2025-12-12',
            'time': '10:30',
            'notes': 'Routine visit'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Visit.objects.count(), 1)

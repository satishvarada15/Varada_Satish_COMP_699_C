from django.test import TestCase
from django.urls import reverse
from .models import CustomUser, MotherProfile

class MotherRegistrationTest(TestCase):
    def test_mother_registration_creates_profile(self):
        response = self.client.post(reverse('mother_register'), {
            'username': 'testmother',
            'email': 'mother@example.com',
            'password1': 'Strongpass123!',
            'password2': 'Strongpass123!',
            'due_date': '2025-12-31',
            'risk_level': 'High',
            'location': 'Hyderabad'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(username='testmother').exists())
        user = CustomUser.objects.get(username='testmother')
        self.assertTrue(MotherProfile.objects.filter(user=user).exists())

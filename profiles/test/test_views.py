from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from profiles.models import UserProfile

class TestProfileView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='test',
            first_name='Alberto',
            last_name='Contento',
            email='alberto@hotmail.com'
        )
        self.profile = UserProfile.objects.create(user = self.user)

    def test_profile_list_view(self):
        url = reverse('profile_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_profile_detatil_view(self):
        self.client.login(username="test", password="test")#Con esto nos logueamos con el usuario creado arriba
        url = reverse('profile_detail', args=[self.profile.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
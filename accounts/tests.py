from django.test import TestCase, Client
from django.urls import reverse
from .models import User

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Crée des users test
        self.admin = User.objects.create_user(username='admin', password='pass', role='ADMIN')
        self.delegue = User.objects.create_user(username='delegue', password='pass', role='DELEGATE')
        self.eleve = User.objects.create_user(username='eleve', password='pass', role='ELEVE')

    def test_login_admin_redirect(self):
        response = self.client.post(reverse('login'), {'username':'admin','password':'pass'})
        self.assertRedirects(response, reverse('admin_dashboard'))

    def test_login_delegue_redirect(self):
        response = self.client.post(reverse('login'), {'username':'delegue','password':'pass'})
        self.assertRedirects(response, reverse('delegue_page'))

    def test_login_eleve_redirect(self):
        response = self.client.post(reverse('login'), {'username':'eleve','password':'pass'})
        self.assertRedirects(response, reverse('eleve_page'))

    def test_logout(self):
        self.client.login(username='admin', password='pass')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

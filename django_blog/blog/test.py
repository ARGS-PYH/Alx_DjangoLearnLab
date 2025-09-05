from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(TestCase):
    def test_register_login_logout_flow(self):
        resp = self.client.post(reverse('register'), {
            "username": "tester",
            "email": "t@example.com",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
        })
        self.assertEqual(resp.status_code, 302)

        login = self.client.login(username="tester", password="complexpassword123")
        self.assertTrue(login)

        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 200)
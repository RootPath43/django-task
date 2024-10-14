from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class LoginAPITestCase(APITestCase):
    def setUp(self):
        # Kullanıcı oluşturuluyor
        self.username = "testuser"
        self.password = "password123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = APIClient()

    def test_login_success(self):
        """Geçerli kullanıcı bilgileriyle başarılı bir giriş yapılmasını test eder."""
        data = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post('/api/login/', data, format='json')
        
        # Durum kodu 200 olmalı ve bir token dönmeli
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

        # Token'ın doğru kullanıcıya ait olup olmadığını kontrol et
        token = response.data['token']
        token_obj = Token.objects.get(key=token)
        self.assertEqual(token_obj.user, self.user)


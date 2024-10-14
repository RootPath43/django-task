from django.test import TestCase
from django.urls import reverse

class LoginPageViewTest(TestCase):
    
    def test_get_login_page(self):
        # URL'inizi test etmek için reverse kullanabilirsiniz.
        response = self.client.get(reverse('pages:login-page'))
        
        # Sayfanın başarıyla döndüğünü kontrol eder.
        self.assertEqual(response.status_code, 200)
        
        # Doğru şablonun render edildiğini kontrol eder.
        self.assertTemplateUsed(response, 'login.html')
        
        # Sayfa içeriğinde belirli bir metnin bulunup bulunmadığını kontrol edebilirsiniz.
        self.assertContains(response, "Login")

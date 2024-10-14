from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

class DashboardPageViewTest(TestCase):
    
    def setUp(self):
        # Kullanıcı ve grup oluştur
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(name='TestGroup')
        self.user.groups.add(self.group)
    
    def test_dashboard_page_authenticated_user(self):
        # Kullanıcıyı giriş yapmış olarak ayarla
        self.client.login(username='testuser', password='testpassword')
        
        # Sayfaya GET isteği yap
        response = self.client.get(reverse('pages:dashboard'))
        
        # Başarılı dönüş olup olmadığını kontrol et
        self.assertEqual(response.status_code, 200)
        
        # Doğru şablonun render edildiğini kontrol et
        self.assertTemplateUsed(response, 'dashboard.html')
        
        # Şablonun context içinde doğru grubun gönderildiğini kontrol et
        self.assertEqual(response.context['group'], self.group)

    def test_dashboard_page_redirects_for_unauthenticated_user(self):
        # Giriş yapmadan sayfaya GET isteği yap
        response = self.client.get(reverse('pages:dashboard'))
        
        # Giriş yapmamış kullanıcılar için yönlendirme olmalıdır (örneğin, login sayfasına)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(''))

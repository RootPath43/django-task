from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from api.models import Aircraft

class AddPageViewTest(TestCase):
    
    def setUp(self):
        # Kullanıcı ve grup oluştur
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(name='TestGroup')
        self.user.groups.add(self.group)
        
        # Örnek Aircraft nesnesi oluştur
        self.aircraft = Aircraft.objects.create(
            aircraft_id=1,
            aircraft_name='Test Aircraft'
        )

    def test_add_page_authenticated_user(self):
        # Kullanıcıyı giriş yapmış olarak ayarla
        self.client.login(username='testuser', password='testpassword')
        
        # Sayfaya GET isteği yap
        response = self.client.get(reverse('pages:add'))
        
        # Başarılı dönüş olup olmadığını kontrol et
        self.assertEqual(response.status_code, 200)
        
        # Doğru şablonun render edildiğini kontrol et
        self.assertTemplateUsed(response, 'add.html')
        
        # Kontekste aircrafts listesinin olduğunu kontrol et
        self.assertIn('aircrafts', response.context)
        self.assertIn(self.aircraft, response.context['aircrafts'])
        
        # Kontekste kullanıcı grubunun olduğunu kontrol et
        self.assertEqual(response.context['group'], self.group)

    def test_add_page_redirects_for_unauthenticated_user(self):
        # Giriş yapmadan sayfaya GET isteği yap
        response = self.client.get(reverse('pages:add'))
        
        # Giriş yapmamış kullanıcılar için yönlendirme olmalıdır (örneğin, login sayfasına)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(''))

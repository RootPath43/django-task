from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from api.models import Aircraft, ProducedPart, Production, Part
from api.serializer import ProducedPartSerializer, ProductionSerializer

class UpdatePageViewTest(TestCase):
    
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
        self.part=Part.objects.create(
            part_id=1,
            part_name="Wing"
        )
        
        # Örnek ProducedPart nesnesi oluştur
        self.part = ProducedPart.objects.create(
            produced_part_id=1,
            part=self.part,  # İlişki için uygun bir örnek
            is_used=False,
            aircraft=self.aircraft,
            producer=self.user
        )
        
        # Örnek Production nesnesi oluştur
        self.production = Production.objects.create(
            product_id=1,
            aircraft=self.aircraft,
            used_wing=self.part,
            used_fuselage=self.part,
            used_tail=self.part,
            used_avionics=self.part,
            is_produced=True,
            producer=self.user
        )

    def test_update_page_authenticated_user_with_produced_part(self):
        # Kullanıcıyı giriş yapmış olarak ayarla
        self.client.login(username='testuser', password='testpassword')
        
        # Sayfaya GET isteği yap
        response = self.client.get(reverse('pages:update-page', kwargs={'pk': self.part.produced_part_id}))
        
        # Başarılı dönüş olup olmadığını kontrol et
        self.assertEqual(response.status_code, 200)
        
        # Doğru şablonun render edildiğini kontrol et
        self.assertTemplateUsed(response, 'update.html')
        
        # Kontekste verinin bulunduğunu kontrol et
        self.assertIn('data', response.context)
        self.assertIn('aircrafts', response.context)
        self.assertIn('group', response.context)
        
        # Verinin doğru şekilde serileştirildiğini kontrol et
        serialized_part = ProducedPartSerializer(self.part).data
        self.assertJSONEqual(response.context['data'], serialized_part)

    def test_update_page_authenticated_user_with_production(self):
        # Kullanıcıyı giriş yapmış olarak ayarla
        self.client.login(username='testuser', password='testpassword')
        
        # Kullanıcı grubunu Assembly olarak ayarla
        assembly_group = Group.objects.create(name='Assembly')
        self.user.groups.add(assembly_group)

        # Sayfaya GET isteği yap
        response = self.client.get(reverse('pages:update-page', kwargs={'pk': self.production.product_id}))
        
        # Başarılı dönüş olup olmadığını kontrol et
        self.assertEqual(response.status_code, 200)
        
        # Doğru şablonun render edildiğini kontrol et
        self.assertTemplateUsed(response, 'update.html')
        
        # Kontekste verinin bulunduğunu kontrol et
        self.assertIn('data', response.context)
        self.assertIn('aircrafts', response.context)
        self.assertIn('group', response.context)

  

    def test_update_page_redirects_for_unauthenticated_user(self):
        # Giriş yapmadan sayfaya GET isteği yap
        response = self.client.get(reverse('pages:update-page', kwargs={'pk': self.part.produced_part_id}))
        
        # Giriş yapmamış kullanıcılar için yönlendirme olmalıdır (örneğin, login sayfasına)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(''))


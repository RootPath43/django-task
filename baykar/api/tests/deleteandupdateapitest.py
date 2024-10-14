from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from api.models import ProducedPart, Production, Aircraft, Part

class DeleteAndUpdateAPITestCase(APITestCase):
    def setUp(self):
        # Kullanıcı ve grup oluşturuluyor
        self.username = "testuser"
        self.password = "password123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.group = Group.objects.create(name="Wing")
        self.user.groups.add(self.group)

        # Token oluşturuluyor
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Aircraft ve Part verisi oluşturuluyor
        self.aircraft = Aircraft.objects.create(aircraft_name="TB2")
        self.new_aircraft = Aircraft.objects.create(aircraft_name="TB3")
        self.part = Part.objects.create(part_name="Wing")
        self.produced_part = ProducedPart.objects.create(
            part=self.part,
            aircraft=self.aircraft,
            producer=self.user,
            is_used=False
        )
        self.production = Production.objects.create(
            aircraft=self.aircraft,
            used_wing=self.produced_part,
            used_fuselage=self.produced_part,
            used_tail=self.produced_part,
            used_avionics=self.produced_part,
            is_produced=True,
            producer=self.user
        )

    def test_update_produced_part(self):
        """Kullanıcının ürettiği parçayı güncelleme işlemini test eder."""
        data = {
            "aircraft": self.new_aircraft.aircraft_id
        }
        response = self.client.patch(f'/api/dashboard/{self.produced_part.produced_part_id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        
        # Güncellemenin doğru yapıldığını kontrol et
        self.produced_part.refresh_from_db()
        self.assertEqual(self.produced_part.aircraft, self.new_aircraft)

    def test_update_production(self):
        """Kullanıcının ürettiği üretimi güncelleme işlemini test eder."""
        # Kullanıcıyı "Assembly" grubuna ekle
        self.user.groups.clear()
        self.user.groups.add(Group.objects.create(name="Assembly"))

        data = {
            "aircraft": self.new_aircraft.aircraft_id
        }
        response = self.client.patch(f'/api/dashboard/{self.production.product_id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        
        # Güncellemenin doğru yapıldığını kontrol et
        self.production.refresh_from_db()
        self.assertEqual(self.production.aircraft, self.new_aircraft)

   
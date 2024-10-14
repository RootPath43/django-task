from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from api.models import Part, ProducedPart, Production, Aircraft

class DashboardAPITestCase(APITestCase):
    def setUp(self):
        # Kullanıcı ve grup oluşturuluyor
        self.user = User.objects.create_user(username="testuser", password="password")
        self.assembly_group = Group.objects.create(name="Assembly")
        self.part_group = Group.objects.create(name="Wing")
        self.user.groups.add(self.part_group)

        # Token oluşturuluyor
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Aircraft ve Part verisi oluşturuluyor
        self.aircraft = Aircraft.objects.create(aircraft_name="TB2")
        self.part = Part.objects.create(part_name="Wing")
        self.produced_part = ProducedPart.objects.create(
            part=self.part,
            aircraft=self.aircraft,
            producer=self.user,
            is_used=False
        )
    
    def test_get_parts_list(self):
        """Parça grubuna sahip kullanıcı için doğru parçaların döndüğünü test eder."""
        response = self.client.get('/api/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["part"]["part_name"], "Wing")

    def test_get_production_list(self):
        """Assembly grubundaki kullanıcı için doğru üretim listesinin döndüğünü test eder."""
        self.user.groups.clear()
        self.user.groups.add(self.assembly_group)
        
        response = self.client.get('/api/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)  # Başlangıçta üretim yok
    
    def test_post_produce_part(self):
        """Parça grubuna sahip kullanıcı için yeni parça üretiminin başarılı olduğunu test eder."""
        data = {
            "aircraft": self.aircraft.aircraft_id
        }
        response = self.client.post('/api/dashboard/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Success")
        self.assertEqual(ProducedPart.objects.filter(part=self.part).count(), 2)

    def test_post_assemble_product(self):
        """Assembly grubundaki kullanıcı için başarılı bir uçak montajını test eder."""
        # Kullanıcıyı Assembly grubuna ekleyin
        self.user.groups.clear()
        self.user.groups.add(self.assembly_group)

        # Gerekli tüm parçaları oluşturun
        Part.objects.bulk_create([
            Part(part_name="Fuselage"),
            Part(part_name="Tail"),
            Part(part_name="Avionics")
        ])
        ProducedPart.objects.bulk_create([
            ProducedPart(part=Part.objects.get(part_name="Fuselage"), aircraft=self.aircraft, producer=self.user, is_used=False),
            ProducedPart(part=Part.objects.get(part_name="Tail"), aircraft=self.aircraft, producer=self.user, is_used=False),
            ProducedPart(part=Part.objects.get(part_name="Avionics"), aircraft=self.aircraft, producer=self.user, is_used=False)
        ])

        data = {
            "aircraft": self.aircraft.aircraft_id
        }
        response = self.client.post('/api/dashboard/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Success")
        self.assertEqual(Production.objects.filter(aircraft=self.aircraft).count(), 1)
        self.assertTrue(Production.objects.first().is_produced)

    def test_post_assemble_product_failure(self):
        """Gerekli parçalar eksik olduğunda montajın başarısız olduğunu test eder."""
        self.user.groups.clear()
        self.user.groups.add(self.assembly_group)

        # Sadece kanat parçası var, diğerleri yok
        data = {
            "aircraft": self.aircraft.aircraft_id
        }
        response = self.client.post('/api/dashboard/', data, format='json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data["message"], "Not enough aircraft part")

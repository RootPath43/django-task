from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Part, ProducedPart, Aircraft, Production

class PartTestCase(TestCase):
    def setUp(self):
        Part.objects.create(part_name="Wing")
        Part.objects.create(part_name="Fuselage")
    
    def test_part_creation(self):
        wing = Part.objects.get(part_name="Wing")
        fuselage = Part.objects.get(part_name="Fuselage")
        self.assertEqual(wing.part_name, "Wing")
        self.assertEqual(fuselage.part_name, "Fuselage")


class AircraftTestCase(TestCase):
    def setUp(self):
        Aircraft.objects.create(aircraft_name="TB2")
        Aircraft.objects.create(aircraft_name="AKINCI")
    
    def test_aircraft_creation(self):
        tb2 = Aircraft.objects.get(aircraft_name="TB2")
        akinici = Aircraft.objects.get(aircraft_name="AKINCI")
        self.assertEqual(tb2.aircraft_name, "TB2")
        self.assertEqual(akinici.aircraft_name, "AKINCI")


class ProducedPartTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.aircraft = Aircraft.objects.create(aircraft_name="TB2")
        self.part = Part.objects.create(part_name="Wing")
        self.produced_part = ProducedPart.objects.create(
            part=self.part,
            is_used=False,
            aircraft=self.aircraft,
            producer=self.user
        )
    
    def test_produced_part_creation(self):
        self.assertEqual(self.produced_part.part.part_name, "Wing")
        self.assertFalse(self.produced_part.is_used)
        self.assertEqual(self.produced_part.aircraft.aircraft_name, "TB2")
        self.assertEqual(self.produced_part.producer.username, "testuser")


class ProductionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.aircraft = Aircraft.objects.create(aircraft_name="TB2")
        self.part_wing = Part.objects.create(part_name="Wing")
        self.part_fuselage = Part.objects.create(part_name="Fuselage")
        self.part_tail = Part.objects.create(part_name="Tail")
        self.part_avionics = Part.objects.create(part_name="Avionics")

        # Create ProducedParts
        self.produced_wing = ProducedPart.objects.create(
            part=self.part_wing,
            aircraft=self.aircraft,
            producer=self.user
        )
        self.produced_fuselage = ProducedPart.objects.create(
            part=self.part_fuselage,
            aircraft=self.aircraft,
            producer=self.user
        )
        self.produced_tail = ProducedPart.objects.create(
            part=self.part_tail,
            aircraft=self.aircraft,
            producer=self.user
        )
        self.produced_avionics = ProducedPart.objects.create(
            part=self.part_avionics,
            aircraft=self.aircraft,
            producer=self.user
        )

        # Create Production
        self.production = Production.objects.create(
            aircraft=self.aircraft,
            used_wing=self.produced_wing,
            used_fuselage=self.produced_fuselage,
            used_tail=self.produced_tail,
            used_avionics=self.produced_avionics,
            is_produced=True,
            producer=self.user
        )
    
    def test_production_creation(self):
        self.assertEqual(self.production.aircraft.aircraft_name, "TB2")
        self.assertTrue(self.production.is_produced)
        self.assertEqual(self.production.used_wing.part.part_name, "Wing")
        self.assertEqual(self.production.used_fuselage.part.part_name, "Fuselage")
        self.assertEqual(self.production.used_tail.part.part_name, "Tail")
        self.assertEqual(self.production.used_avionics.part.part_name, "Avionics")
        self.assertEqual(self.production.producer.username, "testuser")

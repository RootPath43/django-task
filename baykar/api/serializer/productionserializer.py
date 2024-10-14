
from rest_framework import serializers
from api.serializer.partserializer import PartSerializer
from api.serializer.aircraftserializer import AircraftSerializer
from api.serializer.userserializer import UserSerializer
from api.serializer.producedpartserializer import ProducedPartSerializer
from api.models import Production

#üretilen uçaklar için serializer
class ProductionSerializer(serializers.ModelSerializer):
    #foreigkey objelerini getiriyoruz
    used_wing =ProducedPartSerializer()
    used_fuselage= ProducedPartSerializer()
    used_tail= ProducedPartSerializer()
    used_avionics= ProducedPartSerializer()
    #uçak ismi objesi
    aircraft=AircraftSerializer()
    #üreten kişi objesi
    producer= UserSerializer()
    
    #üretilme zamanını daha okunur hale getirme
    produced_time=serializers.DateTimeField(format="%d/%b/%Y %H:%M",)
    class Meta:
        model = Production
        fields = '__all__'

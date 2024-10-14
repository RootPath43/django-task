from rest_framework import serializers
from api.models import ProducedPart
from api.serializer.partserializer import PartSerializer
from api.serializer.aircraftserializer import AircraftSerializer
from api.serializer.userserializer import UserSerializer

#üretilen uçak parçaları için serializer
class ProducedPartSerializer(serializers.ModelSerializer):
    #foreign key olarak bağlı objeler getirilir.
    part=PartSerializer()
    aircraft=AircraftSerializer()
    producer=UserSerializer()
    #üretilme zamanını daha okunur hale getirme
    produced_time=serializers.DateTimeField(format="%d/%b/%Y %H:%M",)
    
    class Meta:
        model = ProducedPart
        fields = '__all__'
        
from rest_framework import serializers
from api.models import Aircraft

#uçak isimleri için serializer
class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ["aircraft_name","aircraft_id"]
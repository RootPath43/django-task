from rest_framework import serializers
from api.models import Part

#parça isimleri için serializer
class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ["part_name"]
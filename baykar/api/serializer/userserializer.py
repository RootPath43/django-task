from django.contrib.auth.models import User
from rest_framework import serializers

#kullanıcı için serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name'] 
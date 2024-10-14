from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from django.contrib.auth import login
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

#login yapılır ve token karşıya iletilir
class LoginAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    @swagger_auto_schema(
        operation_description="Bu API, Giriş yapan kullanıcının giriş bilgilerini kontrol eder ve geriye token gönderir.",
        responses={200: openapi.Response('Başarılı'),
                   401:  openapi.Response('Invalid credentials')},
    )
    def post(self, request):
        # Your authentication logic here
        user = authenticate(username=request.data['username'], password=request.data['password'])
        login(request, user)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({'token': token.key}, status=200)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
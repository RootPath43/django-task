from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from api.models import (
    ProducedPart,
    Production,
    Aircraft
)
from django.db.models import Q
from api.serializer import (
    ProducedPartSerializer,
    ProductionSerializer
)
# burası tetiklendiğinde girilen parça silinir ya da güncellenir
# aynı şekilde birleştirilmiş uçak için de geçerlidir


class DeleteAndUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    def get_group(self):

        # kullanıcının ekibi elde edilir.
        group_name = self.request.user.groups.all()[0].name
        return group_name

    def get_object(self, pk, group):
        query_object = None
        if group != "Assembly":
            # assembly grubu harici  gruptan kullanıcının ürettiği parçalara erişilir
            query_object = ProducedPart.objects.select_related("producer", "part", "aircraft").filter(
                Q(produced_part_id=pk) & Q(producer=self.request.user))
        else:
            # assembly grubu  kullanıcının ürettiği parçalara erişilir
            query_object = Production.objects.select_related("producer", "aircraft").filter(
                Q(product_id=pk) & Q(producer=self.request.user))
        return query_object

    def patch(self, request, *args, **kwargs):
        group = self.get_group()

        pk = kwargs.get('pk')

        query_object = self.get_object(pk, group)
        if len(query_object) > 0:
            aircraft_obj = self.get_aircraft_object(request.data["aircraft"])
            # uçak modeli değişitirilir
            query_object[0].aircraft = aircraft_obj
            query_object[0].save()

            return Response(status=200)
        else:
            return Response(status=500)

    def get_aircraft_object(self, pk):
        # var olan  uçak modeli alınır
        aircraft_obj = Aircraft.objects.get(aircraft_id=int(pk))

        return aircraft_obj

    def delete(self, request, *args, **kwargs):
        group = self.get_group()

        pk = kwargs.get('pk')
        query_object = self.get_object(pk, group)

        if len(query_object) > 0:
            query_object[0].delete()
            return Response(status=200)
        else:
            return Response(status=404)

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from api.models import (
    ProducedPart,
    Production,
    Part,
    Aircraft
)
from rest_framework import status, permissions
from api.serializer.producedpartserializer import ProducedPartSerializer
from api.serializer.productionserializer import ProductionSerializer
from django.db.models import Q

# dashboar içi doldurlur. ve yeni eklenecek veriler buraya post req ile gelir


class DashboardAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:

            group_name = self.get_group()
            # kullanıcı hangi ekipte ise ona göre liste döndürülecektir
            if group_name != "Assembly":
                parts_list = ProducedPart.objects.select_related(
                    "part", "producer", "aircraft").filter(part__part_name=group_name)
                # var olan parçalar serializera gönderilir
                serialized = ProducedPartSerializer(parts_list, many=True)

            else:
                production_list = Production.objects.select_related(
                    "used_wing", "used_fuselage", "used_tail",
                    "used_avionics", "producer").all()
                # birleştirilmiş uçaklar serializera gönderilir
                serialized = ProductionSerializer(production_list, many=True)

            return Response(serialized.data, status=status.HTTP_200_OK)

        except Exception as err:

            return Response(status=500)

    def get_group(self):
        # kullanıcının ekibi elde edilir.
        group_name = self.request.user.groups.all()[0].name
        return group_name

    def post(self, request, *args, **kwargs):  # yeni obje oluşturulduğunda tetiklenen yer
        group = self.get_group()
        if group != "Assembly":

            result = self.produce_part(request, group)
            if result:
                return Response({"message": "Success"}, status=200)
            else:
                return Response({"message": "Fail"}, status=200)
        else:
            result = self.assemble_product(request, group)
            if result:
                return Response({"message": "Success"}, status=200)

        return Response({"message": "Not enough aircraft part"}, status=500)

    def produce_part(self, request, group):
        try:
            part = Part.objects.get(part_name=group)  # part objesi alınır
            aircraft = Aircraft.objects.get(
                aircraft_id=request.data["aircraft"])
            new_part = ProducedPart(  # üretilen parça objesi oluşturulur
                part=part,
                is_used=False,
                aircraft=aircraft,
                producer=request.user

            )
            new_part.save()
            return True
        except Exception as err:
            print(err)
            return False

    def assemble_product(self, request, group):
        # üretilmek istenen uçak objesi çağırılır
        aircraft = Aircraft.objects.get(aircraft_id=request.data["aircraft"])
        # uçak parçalarının hepsi alınır
        all_parts = Part.objects.all()
        # uçağın kullanılmamış parçaları dbden çekilir
        unused_parts = ProducedPart.objects.select_related(
            "aircraft", "part").filter(aircraft=aircraft, is_used=False)

        if set(all_parts.values_list("part_name", flat=True)) == set(unused_parts.values_list("part__part_name", flat=True)):
            try:
                parts = {}  # birleştirilecek uçak parçalarının bulunacağı dict
                for unused_part in unused_parts:
                    for part in all_parts:
                        if unused_part.part.part_name == part.part_name and part.part_name not in parts:
                            unused_part.is_used = True
                            unused_part.save()
                            parts[part.part_name] = unused_part
                new_production = Production(
                    aircraft=aircraft,
                    used_wing=parts["Wing"],
                    used_fuselage=parts["Fuselage"],
                    used_tail=parts["Tail"],
                    used_avionics=parts["Avionics"],
                    is_produced=True,
                    producer=request.user
                )
                new_production.save()
                return True
            except Exception as err:
                print(err)
                return False

        else:

            return False

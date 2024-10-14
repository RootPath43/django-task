from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from api.models import (
    ProducedPart,
    Production,
    Aircraft,
    Part
)
from django.db.models import Q
from api.serializer import (
    ProducedPartSerializer,
    ProductionSerializer)
import json


class UpdatePageView(LoginRequiredMixin, View):
    template_name = 'update.html'  # Kullanmak istediğiniz şablonun yolu

    def get(self, request, *args, **kwargs):
        # güncellenecek verinin pksi alınır
        self.pk = kwargs.get('pk')  # pk değerini al
        
        #formda gösterilecek olan bütün değerler çekilir
        aircrafts=Aircraft.objects.all()

        # kullanıcının grubuna göre jinjaya değişken gönderilir ve ona göre html düzenlenir
        user_group = request.user.groups.all()[0].name
        
        if user_group != "Assembly":
            
            #assembly ekibi dışındaki kullanıcıların parçayı kendi ürettiyse güncelleyeiblir.
            try:
                part = ProducedPart.objects.select_related("part", "aircraft").get(
                    Q(producer=request.user) & Q(produced_part_id=self.pk))
                serialized = ProducedPartSerializer(part)
            except:
                return redirect('api:dashboard')
        else:
            #assembly ekibinde bulunan eğer uçağı kendisi ürettiyse uçağı güncellenebilir
            try:
                production = Production.objects.select_related("aircraft").get(
                    Q(producer=request.user) & Q(product_id=self.pk)
                )
                serialized= ProductionSerializer(production)
            except:
                return redirect('api:dashboard')

        return render(request, 
                    template_name=self.template_name, 
                    context={"data": json.dumps(serialized.data),
                             "aircrafts":aircrafts,
                             "group":user_group})

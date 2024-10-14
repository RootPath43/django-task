from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from api.models import (
    Aircraft,
)
from django.db.models import Q


class AddPageView(LoginRequiredMixin, View):
    template_name = 'add.html'  # Kullanmak istediğiniz şablonun yolu

    def get(self, request, *args, **kwargs):
        # güncellenecek verinin pksi alınır
        self.pk = kwargs.get('pk')  # pk değerini al

        # formda gösterilecek olan bütün değerler çekilir

        aircrafts = Aircraft.objects.all()

        # kullanıcının grubuna göre jinjaya değişken gönderilir ve ona göre html düzenlenir
        user_group = request.user.groups.all()[0]

        return render(request,
                      template_name=self.template_name,
                      context={"aircrafts": aircrafts,
                               "group": user_group})

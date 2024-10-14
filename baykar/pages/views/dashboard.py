from django.contrib import messages
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardPageView(LoginRequiredMixin,View):
    template_name = 'dashboard.html'  # Kullanmak istediğiniz şablonun yolu
    
    def get(self, request, *args, **kwargs):
        #kullanıcının grubuna göre jinjaya değişken gönderilir ve ona göre html düzenlenir
        user_group=request.user.groups.all()[0]
        return render(request, template_name=self.template_name,context={"group":user_group})
    
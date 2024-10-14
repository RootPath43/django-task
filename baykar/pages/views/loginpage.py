from django.contrib import messages
from django.views import View
from django.shortcuts import render

class LoginPageView(View):
    template_name = 'login.html'  
    
    def get(self, request, *args, **kwargs):
        #login html çalıştırılır
        return render(request, template_name=self.template_name)
    

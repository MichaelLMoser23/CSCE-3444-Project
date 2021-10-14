from django.shortcuts import render
from django.views import View

#class Index(View):
 #   def get(self, request, *args, **kwargs):
  #      return render(request, 'home/index.html')

class Home(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home/home.html')

class Registration(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home/registration.html')
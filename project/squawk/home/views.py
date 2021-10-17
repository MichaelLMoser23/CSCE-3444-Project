from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home/index.html')

class Login(View):
    def get(self, request):
        return render(request, 'home/login.html')

class Registration(View):
    def get(self, request):
        return render(request, 'home/registration.html')
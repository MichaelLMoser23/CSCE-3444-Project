from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home/index.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out."))
    return redirect('index')


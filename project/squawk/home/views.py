from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home/index.html')

class Login(View):
    def get(self, request):
        return render(request, 'home/login.html')

    def post(self, request):
        return render(request, 'home/login.html')

    def login_user(request):
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                #return redirect('index')
                return redirect('index')
            else:
                # Return an 'invalid login' error message.
                messages.success(request, ("There was an error logging in. Try again."))
                return redirect('login')
        else:
            return render(request, 'home/index.html', {})

class Registration(View):
    def get(self, request):
        return render(request, 'home/registration.html')

    def post(self, request):
        return render(request, 'home/registration.html')

    def register_user(request):
        form = UserCreationForm()

        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
        context = {'form':form}
        return render(request, 'home/registration.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out."))
    return redirect('index')


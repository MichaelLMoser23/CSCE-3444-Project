from django.urls import path
from home import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('home/', views.Login.as_view(), name='login'),
    path('home/registration', views.Registration.as_view(), name='registration'),
]
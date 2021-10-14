from django.urls import path
from . import views

urlpatterns = [
    #path('', views.Index.as_view(), name='index'),
    path('', views.Home.as_view(), name='home'),
    path('', views.Registration.as_view(), name='registration'),
]
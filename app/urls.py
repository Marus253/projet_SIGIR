# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('connexion/usager/', views.login_usager, name='login_usager'),
]

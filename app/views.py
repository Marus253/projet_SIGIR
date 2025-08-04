# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import LoginForm
from .models import Usager
from django.contrib import messages
from django.contrib.auth import authenticate

def login_usager(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data['telephone']
            password = form.cleaned_data['password']
            user = authenticate(request, telephone=telephone, password=password)

            if user is not None and hasattr(user, 'usager'):
                login(request, user)
                messages.success(request, f"Bienvenue {user.get_full_name()}")
                return redirect('accueil_usager')  # Redirige vers la bonne page
            else:
                messages.error(request, "Numéro ou mot de passe incorrect")
    return render(request, 'auth/login.html', {'form': form, 'user_type': 'usager'})

# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from accounts.decorators import role_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if user.role == 'ADMIN':
                return HttpResponseForbidden("Veuillez utiliser l'accès administrateur")

            login(request, user)

            remember_me = request.POST.get('remember_me')
            request.session.set_expiry(1209600 if remember_me else 0)

            if user.role == 'DELEGATE' or user.role == 'SUPPLEANT':
                return redirect('delegue_page')
            elif user.role == 'ELEVE':
                return redirect('eleve_page')

            messages.error(request, "Rôle inconnu")

        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")

    return render(request, 'accounts/login.html')


# -----------------------
# LOGOUT
# -----------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# -----------------------
# PAGES PAR ROLE
# -----------------------
@login_required
def delegue_page(request):
    if request.user.role not in ['DELEGATE', 'SUPPLEANT']:
        return HttpResponseForbidden("Accès refusé")
    return render(request, 'accounts/delegue.html')


@role_required('ELEVE')
def eleve_page(request):
    if request.user.role != 'ELEVE':
        return HttpResponseForbidden("Accès refusé")
    return render(request, 'accounts/eleve.html')


def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            if user.role != 'ADMIN':
                return HttpResponseForbidden("Accès réservé à l'administrateur")

            login(request, user)

            return redirect('ajout_eleve')

        messages.error(request, "Identifiants incorrects")

    return render(request, 'accounts/admin_login.html')


@login_required
def admin_view(request):
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden("Accès réservé à l'administrateur")

    return redirect('ajout_eleve')

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
            login(request, user)

            remember_me = request.POST.get('remember_me')

            if not remember_me:
                request.session.set_expiry(0)  # session expire à la fermeture du navigateur
            else:
                request.session.set_expiry(1209600)  # 2 semaines

            # Redirection selon le rôle stocké dans user.role
            # Ici on suppose que le User a un champ role ou une propriété définie ailleurs
            role = getattr(user, 'role', None)
            if role == 'ADMIN':
                return redirect('admin_dashboard')
            elif role == 'DELEGATE':
                return redirect('delegue_page')
            elif role == 'ELEVE':
                return redirect('eleve_page')
            else:
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
@role_required('ADMIN')
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden("Accès refusé")
    return render(request, 'accounts/admin_dashboard.html')

@role_required('DELEGATE')
def delegue_page(request):
    if request.user.role != 'DELEGATE':
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

            # ✅ redirection vers le dashboard → ajout élève
            return redirect('ajout_eleve')

        messages.error(request, "Identifiants incorrects")

    return render(request, 'accounts/admin_login.html')
def admin_view(request):
    # 🔐 Pas connecté → login admin
    if not request.user.is_authenticated:
        return redirect('admin_login')

    # ❌ Mauvais rôle
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden("Accès réservé à l'administrateur")

    # ✅ Admin connecté → dashboard
    return redirect('ajout_eleve')
# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import timezone

from assDashboard.models import Student, Attendance
from accounts.decorators import role_required


# ------------------
# VUE PAGE D'ACCUEIL
#-------------------

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role == 'ADMIN':
        return redirect('/dashboard/')

    if request.user.role in ['DELEGATE', 'SUPPLEANT']:
        return redirect('delegue_page')

    if request.user.role == 'ELEVE':
        return redirect('eleve_page')

    return redirect('login')

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
    etudiant = Student.objects.get(user=request.user)

    return render(request, "accounts/eleve.html", {"etudiant": etudiant})


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


# -----------------------
# SCAN QR — vérification présence avec date
# -----------------------
#def scan_qr(request, token):
#    student = get_object_or_404(Student, qr_token=token)
#
#    today = timezone.now().date()
#
#    # Vérifie si une présence existe déjà aujourd'hui pour cet étudiant
#    deja_present = Attendance.objects.filter(
#        student=student,
#        date__date=today
#    ).exists()
#
#    if deja_present:
#        return HttpResponse(
#            f"⚠️ Présence déjà enregistrée aujourd'hui ({today}) pour {student}.",
#            content_type="text/plain; charset=utf-8"
#        )
#
#    Attendance.objects.create(student=student, date=timezone.now())
#
  #  return HttpResponse(
  #      f"✅ Présence enregistrée pour {student} le {today}.",
  #      content_type="text/plain; charset=utf-8"
  #  )
@login_required
def scan_qr(request, token):

    # 1. Vérification des rôles
    if request.user.role not in ["DELEGATE", "ADMIN","SUPPLEANT"]:
        return HttpResponseForbidden("Accès refusé")

    # 2. Récupération étudiant
    student = get_object_or_404(Student, qr_token=token)

    today = timezone.now().date()

    # 3. Vérifie déjà présent aujourd'hui
    deja_present = Attendance.objects.filter(
        student=student,
        date__date=today
    ).exists()

    if deja_present:
        return HttpResponse(
            f"⚠️ Présence déjà enregistrée aujourd'hui ({today}) pour {student}.",
            content_type="text/plain; charset=utf-8"
        )
    # 4. Création présence
    Attendance.objects.create(
        student=student,
        date=timezone.now()
    )

    return HttpResponse(
        f"✅ Présence enregistrée pour {student} le {today}.",
        content_type="text/plain; charset=utf-8"
    )        

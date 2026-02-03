from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from accounts.decorators import role_required
from . import forms
from .forms import StudentCreateForm
from .models import Student

User = get_user_model()

@role_required('ADMIN')
def ajout_eleve(request):
    if request.method == 'POST':
        form = StudentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']  # récupère le mot de passe du formulaire
            role = request.POST.get('role', 'ELEVE')
            # Création du user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
            )

            # Création de l'étudiant et associer au USER de Django
            student = form.save(commit=False)
            student.user = user
            student.save()

            messages.success(request, f"L'élève {username} a été ajouté avec succès.")
            return redirect('ajout_eleve')
    else:
        messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
        form = StudentCreateForm()

    return render(request, 'dashboard/ajout_eleve.html', {'form': form})

@role_required('ADMIN')
def ajout_matiere(request):
    # pour l'instant, on affiche juste un message
    return render(request, 'dashboard/ajout_matiere.html')
@role_required('ADMIN')
def liste_eleves(request):
    students = Student.objects.all()
    return render(request, 'dashboard/liste_eleves.html', {'students': students})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from accounts.decorators import role_required
from .forms import StudentCreateForm
from .models import Student, Matiere, MENTION_CHOICES, LEVEL_CHOICES, Semestre


User = get_user_model()


@role_required('ADMIN')
def ajout_eleve(request):
    if request.method == 'POST':
        form = StudentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = request.POST.get('role', 'ELEVE')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
            )
            student = form.save(commit=False)
            student.user = user
            student.save()

            messages.success(request, f"L'élève {username} a été ajouté avec succès.")
            return redirect('ajout_eleve')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = StudentCreateForm()

    return render(request, 'dashboard/ajout_eleve.html', {'form': form})


@role_required('ADMIN')
def liste_eleves(request):
    etudiants = Student.objects.select_related('user').all()
    annee = request.GET.get('annee')
    mention = request.GET.get('mention')
    if annee:
        etudiants = etudiants.filter(niveau=annee)
    if mention:
        etudiants = etudiants.filter(mention=mention)

    context = {
        'etudiants': etudiants,
        'mentions': MENTION_CHOICES,
        'niveaux': LEVEL_CHOICES,
        'request': request,  # pour utiliser request.GET dans le template
    }
    return render(request, 'dashboard/liste_etudiants_cards.html', context)

@role_required('ADMIN')
def profil_eleves(request, student_id):
    etudiant = get_object_or_404(Student, id=student_id)

    risque_echec_general = 56  # calcul réel ou mock
    risque_echec_matiere = 74  # calcul réel ou mock

    radius = 70
    circumference = 2 * 3.1416 * radius
    dashoffset_general = circumference - (circumference * risque_echec_general / 100)
    dashoffset_matiere = circumference - (circumference * risque_echec_matiere / 100)

    context = {
        "etudiant": etudiant,
        "risque_echec_general": risque_echec_general,
        "risque_echec_matiere": risque_echec_matiere,
        'dashoffset_general': dashoffset_general,
        'dashoffset_matiere': dashoffset_matiere,
    }
    return render(request, 'dashboard/profil_eleve.html', context)

@role_required('ADMIN')
def liste_matieres(request):
    matieres = Matiere.objects.all()

    # GET parameters
    niveau = request.GET.get('id_niveau')
    annee = request.GET.get('annee')
    mention = request.GET.get('id_mention')
    semestre = request.GET.get('id_semestre')
    if annee:
        matieres = matieres.filter(annee=annee)
    if niveau:
        matieres = matieres.filter(niveau=niveau)
    if mention:
        matieres = matieres.filter(mention=mention)
    if semestre:
        matieres = matieres.filter(semestre_id=semestre)

    context = {
        'matieres': matieres,
        'annee': annee,
        'niveau': LEVEL_CHOICES,
        'mentions': MENTION_CHOICES,
        'semestres': Semestre.SEMESTRES,
        'request': request,
    }

    return render(request, 'dashboard/liste_matieres.html', context)

@role_required('ADMIN')
def ajouter_matiere(request):
    mentions = MENTION_CHOICES
    niveaux = LEVEL_CHOICES
    semestres = Semestre.SEMESTRES

    if request.method == "POST":
        nom = request.POST.get("nom_matiere")
        mention = request.POST.get("id_mention")
        niveau = request.POST.get("id_niveau")
        semestre = request.POST.get("id_semestre")
        annee = request.POST.get("annee")

        Matiere.objects.create(
            nom=nom,
            mention=mention,
            niveau=niveau,
            semestre=semestre,
            annee=annee
        )

        messages.success(request, "Matière ajoutée avec succès.")
 #       return redirect("dashboard/ajout_matieres.html")

    return render(request, "dashboard/ajout_matieres.html", {
        "nom": nom,
        "mentions": mentions,
        "niveaux": niveaux,
        "semestres": semestres,
    })
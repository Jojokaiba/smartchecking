from django.shortcuts import render
from .models import EtudiantAll
from .models import MatiereAll

def liste_etudiants_cards(request):
    """
    Affiche la liste des étudiants sous forme de cartes
    avec filtres dynamiques sur Année et Mention.
    """

    # 🔹 1. Récupérer les filtres depuis l'URL (GET)
    annee = request.GET.get('annee')       # Exemple : 'L1', 'L2', 'L3', ou None
    mention = request.GET.get('mention')   # Exemple : 'Informatique', 'Gestion', etc., ou None

    # 🔹 2. Queryset de base : tous les étudiants
    etudiants = EtudiantAll.objects.all()

    # 🔹 3. Appliquer les filtres si ils existent
    if annee:
        etudiants = etudiants.filter(annee=annee)
    if mention:
        etudiants = etudiants.filter(nom_mention=mention)

    # 🔹 4. Envoyer le queryset filtré au template
    return render(request, 'liste_etudiants_cards.html', {
        'etudiants': etudiants
    })


def creation_compte(request):
    """
    Page de création de compte étudiant
    """
    return render(request, 'creation_compte.html')


def liste_matieres(request):
    """
    Page de la liste des matières
    """
    return render(request, 'liste_matieres.html')




def liste_matieres(request):
    matieres = MatiereAll.objects.all()

    annee = request.GET.get('annee')
    mention = request.GET.get('mention')
    semestre = request.GET.get('semestre')

    if annee:
        matieres = matieres.filter(annee=annee)

    if mention:
        matieres = matieres.filter(mention=mention)

    if semestre:
        matieres = matieres.filter(semestre=semestre)

    context = {
        'matieres': matieres,
        'annees': MatiereAll.objects.values_list('annee', flat=True).distinct(),
        'mentions': MatiereAll.objects.values_list('mention', flat=True).distinct(),
        'semestres': MatiereAll.objects.values_list('semestre', flat=True).distinct(),
    }

    return render(request, 'liste_matieres.html', context)


from django.shortcuts import render
from .models import EtudiantAll
from .models import MatiereAll
from django.db import connection
from django.shortcuts import render, redirect



def liste_etudiants_cards(request):
    """
    Affiche la liste des étudiants sous forme de cartes
    avec filtres dynamiques sur Année et Mention.
    """

    annee = request.GET.get('annee')   
    mention = request.GET.get('mention')  

    etudiants = EtudiantAll.objects.all()

    if annee:
        etudiants = etudiants.filter(annee=annee)
    if mention:
        etudiants = etudiants.filter(nom_mention=mention)

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


def ajouter_matiere(request):

    with connection.cursor() as cursor:
        cursor.execute("SELECT id_mention, nom_mention FROM mention")
        mentions = cursor.fetchall()

        cursor.execute("SELECT id_semestre, semestre, annee FROM semestre")
        semestres = cursor.fetchall()

    if request.method == "POST":
        nom_matiere = request.POST.get("nom_matiere")
        id_mention = request.POST.get("id_mention")
        id_semestre = request.POST.get("id_semestre")

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO matiere (nom_matiere, id_mention, id_semestre)
                VALUES (%s, %s, %s)
            """, [nom_matiere, id_mention, id_semestre])

        return redirect("ajouter_matiere")

    return render(request, "ajouter_matiere.html", {
        "mentions": mentions,
        "semestres": semestres
    })


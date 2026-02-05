from django.shortcuts import render

# Create your views here.
def dashboardadmin(request):
    risque_echec_general= 56
    risque_echec_matiere = 74
    nom = "MONG"
    prenom = "Johan"
    matricule = 11
    numero = "034 05 996 18"
    email = "mongjohanandry@gmail.com"
    mention = "Informatique"
    niveau = "L3"
    parcours = "Génie Logiciel"
    role = "étudiant"

    radius = 70
    circumference = 2 * 3.1416 * radius
    dashoffset_general = circumference - (circumference * risque_echec_general / 100)
    dashoffset_matiere = circumference - (circumference * risque_echec_matiere / 100)
    context = {
        "nom": nom,
        "prenom": prenom,
        "matricule": matricule,
        "email": email,
        "numero": numero,
        "mention": mention,
        "niveau": niveau,
        "parcours": parcours,
        "role": role,
        "risque_echec_general": risque_echec_general,
        "risque_echec_matiere":risque_echec_matiere,
        'dashoffset_general': dashoffset_general,
        'dashoffset_matiere': dashoffset_matiere,
    }
    return render(request, "dashboardadmin/index.html", context)
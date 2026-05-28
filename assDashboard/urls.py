# dashboard/urls.py
from django.urls import path
from assDashboard import views

urlpatterns = [
    # Ajout d'élève (admin-dashboard)
    path('creation/', views.ajout_eleve, name='ajout_eleve'),

    # Liste d'élèves (dashboard fusionné)
    path('etudiants/', views.liste_eleves, name='liste_etudiants_cards'),

    # Ajout matière / liste matière (dashboard fusionné)
    path('matieres/', views.liste_matieres, name='liste_matieres'),
    path('matieres/ajouter/', views.ajouter_matiere, name='ajout_matieres'),

    path('profil/<int:student_id>/', views.profil_eleves, name='profil_eleve'),
]

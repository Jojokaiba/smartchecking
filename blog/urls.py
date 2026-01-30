from django.urls import path
from . import views

urlpatterns = [
    path('etudiants/', views.liste_etudiants_cards, name='liste_etudiants'),
    path('creation-compte/', views.creation_compte, name='creation_compte'),
    path('matieres/', views.liste_matieres, name='liste_matieres'),
]

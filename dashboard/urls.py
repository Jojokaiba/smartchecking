from django.urls import path
from . import views

urlpatterns = [
    path('creation/', views.ajout_eleve, name='ajout_eleve'),
    path('liste/', views.liste_eleves, name='liste_eleves'),  # ← ajout
    path('ajout-matiere/', views.ajout_matiere, name='ajout_matiere'),
]

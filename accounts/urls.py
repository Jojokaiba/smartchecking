# accounts/urls.py
from django.urls import path
from . import views  # ici on importe nos vues définies ci-dessus

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('administration/', views.admin_dashboard, name='admin_dashboard'),
    path('delegue/', views.delegue_page, name='delegue_page'),
    path('eleve/', views.eleve_page, name='eleve_page'),
]

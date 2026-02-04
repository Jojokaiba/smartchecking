# accounts/urls.py
from django.urls import path
from . import views  # ici on importe nos vues définies ci-dessus

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path(
        'secure-access/9f3k2-admin/login/',
        views.admin_login_view,
        name='admin_login'
    ),
    path('delegue/', views.delegue_page, name='delegue_page'),
    path('eleve/', views.eleve_page, name='eleve_page'),
]

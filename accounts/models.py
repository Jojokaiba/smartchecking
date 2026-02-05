from django.contrib.auth.models import AbstractUser
from django.db import models

# utilise User de Django et pourra être lié à Student plus tard, juste modele pour les roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('DELEGATE', 'Delegue'),
        ('SUPPLEANT', 'Suppleant'),
        ('ELEVE', 'Élève'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

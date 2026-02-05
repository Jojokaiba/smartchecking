from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    LEVEL_CHOICES = [
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
    ]
    GENRE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student'
    )
    MENTION_CHOICES = [
        ('INFORMATIQUE', 'Informatique & Génie Logiciel'),
        ('ENERGIE RENOUVELABLE', 'Energie Renouvelable'),
        ('INFO-COM', 'Information & Communication'),
        ('ECONOMIE-GESTION', 'Economie & Ingénierie Financière / Gestion'),
        ('RESSOURCES MINERALES', 'Ressources Minérales & Aménagement du sous-sol'),
        ('PACES', 'PACES'),
        ('ANESTHESIE', 'Anesthésie & Réanimation'),
        ('TECH-BIO', 'Technologie Biomédicale'),
    ]
    MENTION_NIVEAUX = {
        'INFORMATIQUE': ['L1', 'L2', 'L3'],
        'ENERGIE RENOUVELABLE': ['L1', 'L2', 'L3'],
        'INFO-COM': ['L3'],
        'ECONOMIE-GESTION': ['L3'],
        'RESSOURCES MINERALES': ['L3'],
        'PACES': ['L1'],
        'ANESTHESIE': ['L2', 'L3'],
        'TECH-BIO': ['L2', 'L3'],
    }
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=150)
    mention = models.CharField(max_length=50, choices=MENTION_CHOICES)
    niveau = models.CharField(max_length=5, choices=LEVEL_CHOICES)
    photo = models.ImageField(upload_to='students/photos/', null=True, blank=True)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES, null=True, blank=True)

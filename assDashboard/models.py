from django.utils import timezone

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

import uuid

User = get_user_model()
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
LEVEL_CHOICES = [
    ('L1', 'Licence 1'),
    ('L2', 'Licence 2'),
    ('L3', 'Licence 3'),
]
# Modèle pour la création d'élève via le dashboard
class Student(models.Model):

    GENRE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student'
    )
    matricule = models.CharField(max_length=50, null=True, blank=True, unique=True)
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=150)
    date_naissance = models.DateField(null=True, blank=True)
    mention = models.CharField(max_length=50, choices=MENTION_CHOICES)
    niveau = models.CharField(max_length=5, choices=LEVEL_CHOICES, default='L1')
    photo = models.ImageField(upload_to='students/photos/', null=True, blank=True)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES, null=True, blank=True)

    qr_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def clean(self):
        if self.niveau not in MENTION_NIVEAUX.get(self.mention, []):
            raise ValidationError(f"Niveau {self.niveau} non autorisé pour la mention {self.mention}")

    def __str__(self):
        return f"{self.nom} {self.prenoms} ({self.matricule})"


# -------------------------
# Modèles Matières
# -------------------------
class Semestre(models.Model):
    SEMESTRES = [
        ('1', 'Semestre 1'),
        ('2', 'Semestre 2'),
    ]

    nom = models.CharField(max_length=2, choices=SEMESTRES, unique=True)

    def __str__(self):
        return self.get_nom_display()


class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    mention = models.CharField(max_length=20, choices=MENTION_CHOICES)
    niveau = models.CharField(max_length=5, choices=LEVEL_CHOICES, default='L1')
    semestre = models.CharField(max_length=2, choices=Semestre.SEMESTRES)
    annee = models.CharField(max_length=10)

    class Meta:
        unique_together = ('nom', 'mention', 'semestre', 'annee')

    def __str__(self):
        mention_affiche = self.get_mention_display()
        return f"{self.nom} ({mention_affiche}, Semestre {self.semestre})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    date = models.DateTimeField(default=timezone.now)
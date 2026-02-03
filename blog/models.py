from django.db import models

class EtudiantAll(models.Model):
    id_etudiant = models.IntegerField(primary_key=True)
    matricule = models.CharField(max_length=50)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    genre = models.CharField(max_length=10)
    nom_mention = models.CharField(max_length=100)
    semestre = models.CharField(max_length=10)
    annee = models.CharField(max_length=10)

    class Meta:
        db_table = 'etudiant_all'
        managed = False


class MatiereAll(models.Model):
    id_matiere = models.IntegerField(primary_key=True)
    matiere = models.CharField(max_length=100)
    mention = models.CharField(max_length=100)
    semestre = models.CharField(max_length=10)
    annee = models.CharField(max_length=10)

    class Meta:
        db_table = 'matiere_all' 
        managed = False
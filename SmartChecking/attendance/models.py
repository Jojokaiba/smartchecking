from django.db import models

# Create your models here.
    # a ajouter aux modele student
        class Student(models.Model):
            student_id = models.CharField(max_length=50, unique=True)
            qr_token = models.UUIDField(default=uuid.uuid4, editable=false, unique=True)
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
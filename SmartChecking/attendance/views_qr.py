from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Student, Presence

def scan_qr(request, token):
    student = get_object_or_404(Student, qr_token=token)

    Presence.objects.create(student=student)

    return HttpResponse(f"Presence enregistree pour {student.name}")
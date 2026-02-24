import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Student

# Create your views here.
def generate_qr(request, student_id):
    # erreur 404 si l'étudiant n'existe pas
    student = get_object_or_404(Student, student_id=student_id)
    
    qr_data = f"/scan/{student.qr_token}"

    qr = qrcode.make(qr_data)

    buffer = BytesIO()

    qr.save(buffer, format="PNG")

    return HttpResponse(buffer.getvalue(), content_type="image/png")
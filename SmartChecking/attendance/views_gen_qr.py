import qrcode
from io import BytesIO
from django.http import HttpResponse
from .models import Student

# Create your views here.
def generate_qr(request, student_id):
    student = Student.object.get(student_id=student_id)
    qr_data = f"http://127.0.0.1:8000/scan/{student.qr_token}"

    qr = qrcode.make(qr_data)

    buffer = BytesIO()

    qr.save(buffer, format="PNG")

    return HttpResponse(buffer.getvalue(), content_type="image/png")
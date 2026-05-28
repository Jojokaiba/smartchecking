import qrcode
from io import BytesIO
from django.http import HttpResponse, Http404
from assDashboard.models import Student


def generate_qr(request, matricule):
    """
    Génère un QR code pour un étudiant identifié par son matricule.
    Le QR encode l'URL de scan (token UUID) utilisable depuis un mobile.
    """
    try:
        student = Student.objects.get(matricule=matricule)
    except Student.DoesNotExist:
        raise Http404("Étudiant introuvable")
    except Student.MultipleObjectsReturned:
        # Fallback : prendre le premier si doublons en base (données existantes)
        student = Student.objects.filter(matricule=matricule).first()

    scan_url = request.build_absolute_uri(f"/accounts/scan/{student.qr_token}/")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(scan_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")

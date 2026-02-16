from django.urls import path
from . import views

urlpatterns = [
    path("generate_qr/<str:student_id>/", views.generate_qr),
    path("scan/<uuid:token>/", views.scan_qr),
]
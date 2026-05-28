from django.urls import path
from . import views

urlpatterns = [
    path('qr/', views.generate_qr, name='generate_qr'),
]
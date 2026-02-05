from django.urls import path
from .views import dashboardadmin

urlpatterns=[
    path('', dashboardadmin, name="dashboardadmin"),
]
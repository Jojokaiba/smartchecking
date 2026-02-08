from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # URLs de l'app accounts
    path('accounts/', include('accounts.urls')),

    # URLs de ton dashboard
    path('dashboard/', include('assDashboard.urls')),
]

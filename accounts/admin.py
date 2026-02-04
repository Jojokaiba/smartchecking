from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    # 🔹 méthodes locales à l’admin
    def nom(self, obj):
        if hasattr(obj, 'student'):
            return obj.student.nom
        return "-"

    nom.short_description = "Nom"

    def prenoms(self, obj):
        if hasattr(obj, 'student'):
            return obj.student.prenoms
        return "-"

    prenoms.short_description = "Prénoms"
    list_display = (
        'username',
        'nom',
        'prenoms',
        'email',
        'role',
        'is_staff',
        'is_active',
    )

    list_filter = ('role', 'is_staff', 'is_active')

    search_fields = ('username', 'email', 'first_name', 'last_name')

    ordering = ('username',)

    # Champs visibles dans la page détail
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Rôle', {'fields': ('role',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Champs visibles lors de la création
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'role',
                'password1',
                'password2',
            ),
        }),
    )


# Register your models here.

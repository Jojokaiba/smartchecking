from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from assDashboard.models import Student, Matiere

#ce qu'on voit dans le dashboard admin de Django
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

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

# -------------------------
# Admin pour Student
# -------------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenoms', 'matricule', 'user', 'mention', 'niveau', 'genre')
    list_filter = ('mention', 'niveau', 'genre')
    search_fields = ('nom', 'prenoms', 'matricule', 'user__username')
    ordering = ('nom',)

# -------------------------
# Admin pour Matiere
# -------------------------
@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'mention_readable', 'niveau', 'semestre_readable', 'annee')
    list_filter = ('mention', 'niveau', 'semestre', 'annee')
    search_fields = ('nom',)

    # Méthodes pour remplacer self.mention.nom et self.semestre.nom
    def mention_readable(self, obj):
        return obj.get_mention_display()
    mention_readable.short_description = "Mention"

    def semestre_readable(self, obj):
        return f"Semestre {obj.semestre}"
    semestre_readable.short_description = "Semestre"
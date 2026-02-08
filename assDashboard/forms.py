from django import forms
from django.contrib.auth import get_user_model

from .models import MENTION_NIVEAUX

from .models import Student, MENTION_CHOICES, LEVEL_CHOICES

User = get_user_model()


class StudentCreateForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur")
    email = forms.EmailField(label="Email de l'étudiant")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    genre = forms.ChoiceField(label="Genre", choices=Student.GENRE_CHOICES)
    mention = forms.ChoiceField(choices=MENTION_CHOICES, label="Mention")
    niveau = forms.ChoiceField(choices=LEVEL_CHOICES, label="Niveau")
    photo = forms.ImageField(label="Photo de l'étudiant", required=True)

    class Meta:
        model = Student
        fields = [
            'username',
            'nom',
            'prenoms',
            'email',
            'genre',
            'mention',
            'niveau',
            'photo',
            'password',

        ]

    # -------------------
    # Validation backend
    # -------------------
    def clean(self):
        cleaned_data = super().clean()
        mention = cleaned_data.get('mention')
        niveau = cleaned_data.get('niveau')

        if mention and niveau:
            niveaux_autorises = MENTION_NIVEAUX.get(mention, [])
            if niveau not in niveaux_autorises:
                raise forms.ValidationError(
                    f"Niveau '{niveau}' invalide pour la mention '{mention}'"
                )
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")  # <-- valide
        return email


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return username

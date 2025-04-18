from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from .models import Profil, Utilisateur, Concours, InfosGenerales, Serie, Mention, Pays, Diplome  # Replace with your actual model name

class CustomTokenObtainPairViewSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Récupère l'email et le mot de passe
        email = attrs.get("email")
        password = attrs.get("password")

        # Cherche l'utilisateur par email
        user = self.user_model.objects.filter(email=email).first()

        if not user or not user.check_password(password) or not user.is_active:
            raise AuthenticationFailed("Email ou mot de passe invalide.")

        # Génère et retourne les tokens avec les informations de l'utilisateur
        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'nom': user.nom,
            'prenom': user.prenom,
            'profil': user.profil.nomProfil,
        }

    @property
    def user_model(self):
        from django.contrib.auth import get_user_model
        return get_user_model()

class ProfilSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Profil
    """
    class Meta:
        model = Profil
        fields = '__all__'  # serialize all the field


class UtilisateurSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Utilisateur
    """
    class Meta:
        model = Utilisateur
        fields = '__all__'  # tserialize all the field
        extra_kwargs = {
            'password': {'write_only':True}
        }

class ConcoursSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Concours
    """
    class Meta:
        model = Concours
        fields = '__all__'  # serialize all the field

class InfosGeneralesSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle InfosGenerales
    """
    class Meta:
        model = InfosGenerales
        fields = '__all__'  # serialize all the field

class SerieSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Serie
    """
    class Meta:
        model = Serie
        fields = '__all__'  # serialize all the field

class MentionSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Mention
    """
    class Meta:
        model = Mention
        fields = '__all__'  # serialize all the field

class PaysSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Pays
    """
    class Meta:
        model = Pays
        fields = '__all__'  # serialize all the field

class DiplomeSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Diplome
    """
    class Meta:
        model = Diplome
        fields = '__all__'  # serialize all the field
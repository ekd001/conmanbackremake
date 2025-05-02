from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from .models import (Profil, Utilisateur, Concours, InfosGenerales, Serie, Mention, Pays, Diplome, 
    Matiere, Note, DiplomeObtenu, Specialite, Dossier, Eleve, Candidat, Parametre, Jury, MembreJury,
    CoefficientMatierePhase
)  # Replace with your actual model name
import datetime
class CustomTokenObtainPairViewSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Récupère l'email et le mot de passe
        code_access = attrs.get("code_access")
        password = attrs.get("password")

        # Cherche l'utilisateur par email
        user = self.user_model.objects.filter(code_access=code_access).first()

        if not user or not user.check_password(password) or not user.is_active:
            raise AuthenticationFailed("Code access ou mot de passe invalide.")
        user.last_login = datetime.datetime.now()
        user.save()

        # Génère et retourne les tokens avec les informations de l'utilisateur
        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'id': user.id,
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
        extra_kwargs = {'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        """
        Override la méthode create pour hasher le mot de passe avant de sauvegarder l'utilisateur
        """
        user = Utilisateur.objects.create_user(**validated_data)
        return user
       

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

class MatiereSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Matiere
    """
    class Meta:
        model = Matiere
        fields = '__all__'  # serialize all the field

class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Note
    """
    class Meta:
        model = Note
        fields = '__all__'  # serialize all the field
        
class DiplomeObtenuSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Diplome Obtenu
    """
    class Meta:
        model = DiplomeObtenu
        fields = '__all__'  # serialize all the field
                
class SpecialiteSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Specialite
    """
    class Meta:
        model = Specialite
        fields = '__all__'  # serialize all the field
                        
class DossierSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Dossier
    """
    class Meta:
        model = Dossier
        fields = '__all__'  # serialize all the field
                                
class EleveSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Eleve
    """
    class Meta:
        model = Eleve
        fields = '__all__'  # serialize all the field
                                        
class CandidatSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Candidat
    """
    class Meta:
        model = Candidat
        fields = '__all__'  # serialize all the field
                         
class ParametreSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Parametre
    """
    class Meta:
        model = Parametre
        fields = '__all__'  # serialize all the field
                                 
class JurySerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Jury
    """
    class Meta:
        model = Jury
        fields = '__all__'  # serialize all the field
                                         
class MembreJurySerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Jury
    """
    class Meta:
        model = MembreJury
        fields = '__all__'  # serialize all the field
                                                 
class CoefficientMatierePhaseSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle CoefficientMatierePhase
    """
    class Meta:
        model = CoefficientMatierePhase
        fields = '__all__'  # serialize all the field
        
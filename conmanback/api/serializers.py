from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from .models import (Profil, Utilisateur, Concours, InfosGenerales, Serie, Mention, Pays, Diplome, 
    Matiere, Note, DiplomeObtenu, Specialite, Dossier, Eleve, Parametre, Jury, MembreJury,
    CoefficientMatierePhase, Candidat, Archivage, Fonctionnalite
)
import datetime

class CustomTokenObtainPairViewSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        # Récupère l'email et le mot de passe
        code_access = attrs .get("code_access")
        password = attrs.get("password")

        # Cherche l'utilisateur par email
        user = self.user_model.objects.filter(code_access=code_access).first()

        if not user or not user.check_password(password) or not user.is_active:
            raise AuthenticationFailed("Code access ou mot de passe invalide.")
        user.last_login = datetime.datetime.now()
        user.save()
        user_data  = UtilisateurSerializer(user).data

        # Génère et retourne les tokens avec les informations de l'utilisateur
        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_data
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


# class UtilisateurSerializer(serializers.ModelSerializer):
#     """
#     Serializer pour le modèle Utilisateur
#     """
#     profil = ProfilSerializer(read_only=True)  # Utiliser le serializer Profil pour le champ profile
#     class Meta:
#         model = Utilisateur
#         fields = '__all__'  # tserialize all the field
#         extra_kwargs = {'password': {'write_only': True}
#         }
    
#     def create(self, validated_data):
#         """
#         Override la méthode create pour hasher le mot de passe avant de sauvegarder l'utilisateur
#         """
#         user = Utilisateur.objects.create_user(**validated_data)
#         return user


class FonctionnalitesSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Concours
    """
    class Meta:
        model = Fonctionnalite
        fields = '__all__'  # serialize all the field

class UtilisateurSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Utilisateur
    """
    profil = serializers.PrimaryKeyRelatedField(
        queryset=Profil.objects.all(),
        write_only=True
    )
    profil_details = ProfilSerializer(source='profil', read_only=True)

    # Pour l'écriture (POST/PUT), on accepte une liste d'IDs
    fonctionnalites = serializers.PrimaryKeyRelatedField(
        queryset=Fonctionnalite.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    # Pour la lecture (GET), on retourne la liste détaillée
    fonctionnalites_details = FonctionnalitesSerializer(source='fonctionnalites', many=True, read_only=True)

    class Meta:
        model = Utilisateur
        fields = [
            'id',
            'nom',
            'prenom',
            'email',
            'telephone',
            'fonctionnalites',         # pour POST/PUT (envoi liste d'IDs)
            'fonctionnalites_details', # pour GET (lecture objets complets)
            'code_access',
            'password',
            'profil',          # pour POST (envoi id)
            'profil_details'   # pour GET (lecture profil complet)
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Utilise le manager personnalisé pour créer un utilisateur
        """
        return Utilisateur.objects.create_user(**validated_data)

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

# class NoteSerializer(serializers.ModelSerializer):
#     """
#     Serializer pour le modèle Note
#     """
#     matiere = MatiereSerializer(read_only=True)
#     class Meta:
#         model = Note
#         fields = '__all__'  # serialize all the field

class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Note
    """
    matiere = serializers.PrimaryKeyRelatedField(
        queryset=Matiere.objects.all(),
        write_only=True
    )
    matiere_details = MatiereSerializer(source='matiere', read_only=True)

    class Meta:
        model = Note
        fields = [
            'id_note',
            'note',
            'est_preselection',
            'matiere',         # pour POST (envoi ID)
            'matiere_details'  # pour GET (lecture objet)
        ]
                
class SpecialiteSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Specialite
    """
    class Meta:
        model = Specialite
        fields = '__all__'  # serialize all the field
                        

# class DiplomeObtenuSerializer(serializers.ModelSerializer):
#     """
#     Serializer pour le modèle Diplome Obtenu
#     """
#     diplome = DiplomeSerializer(read_only=True) 
#     serie = SerieSerializer(read_only=True)
#     pays = PaysSerializer(read_only=True)
#     mention = MentionSerializer(read_only=True)
#     notes = NoteSerializer(many=True, read_only=True)
#     class Meta:
#         model = DiplomeObtenu
#         fields = '__all__'  # serialize all the field

class DiplomeObtenuSerializer(serializers.ModelSerializer):
    # Champs en écriture via ID
    diplome = serializers.PrimaryKeyRelatedField(queryset=Diplome.objects.all(), write_only=True)
    serie = serializers.PrimaryKeyRelatedField(queryset=Serie.objects.all(), write_only=True)
    pays = serializers.PrimaryKeyRelatedField(queryset=Pays.objects.all(), write_only=True)
    mention = serializers.PrimaryKeyRelatedField(queryset=Mention.objects.all(), write_only=True)
    notes = serializers.PrimaryKeyRelatedField(queryset=Note.objects.all(), many=True, write_only=True)

    # Champs en lecture (objets complets)
    diplome_details = DiplomeSerializer(source="diplome", read_only=True)
    serie_details = SerieSerializer(source="serie", read_only=True)
    pays_details = PaysSerializer(source="pays", read_only=True)
    mention_details = MentionSerializer(source="mention", read_only=True)
    notes_details = NoteSerializer(source="notes", many=True, read_only=True)

    class Meta:
        model = DiplomeObtenu
        fields = [
            'id_diplome_obtenu',
            'annee',
            'diplome', 'diplome_details',
            'serie', 'serie_details',
            'pays', 'pays_details',
            'mention', 'mention_details',
            'notes', 'notes_details'
        ]

class DossierSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Dossier
    """
    specialite = SpecialiteSerializer(read_only=True)  # Utiliser le serializer Specialite pour le champ specialite
    diplomes_obtenus = DiplomeObtenuSerializer(many=True, read_only=True) 
    class Meta:
        model = Dossier
        fields = '__all__'  # serialize all the field

class EleveSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Eleve
    """
    dossier = DossierSerializer(read_only=True)  
    pays_naissance = PaysSerializer(read_only=True)
    class Meta:
        model = Eleve
        fields = '__all__'  # serialize all the field
                                 
class CandidatSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Candidat
    """
    eleve = EleveSerializer(read_only=True)
    notes = NoteSerializer(many=True, read_only=True) 
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
                                         
# class MembreJurySerializer(serializers.ModelSerializer):
#     """
#     Serializer pour le modèle Jury
#     """
#     jury = JurySerializer(read_only=True)  
#     class Meta:
#         model = MembreJury
#         fields = '__all__'  # serialize all the field

class MembreJurySerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle MembreJury
    """
    jury = serializers.PrimaryKeyRelatedField(
        queryset=Jury.objects.all(),
        write_only=True
    )
    jury_details = JurySerializer(source='jury', read_only=True)
    
    class Meta:
        model = MembreJury
        fields = ['id_membre', 'nom', 'prenom', 'jury', 'jury_details']
                              
# class CoefficientMatierePhaseSerializer(serializers.ModelSerializer):
#     """
#     Serializer pour le modèle CoefficientMatierePhase
#     """
#     specialite = SpecialiteSerializer(read_only=True)
#     matiere = MatiereSerializer(read_only=True)
#     class Meta:
#         model = CoefficientMatierePhase
#         fields = '__all__'  # serialize all the field

class CoefficientMatierePhaseSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle CoefficientMatierePhase
    """
    specialite = serializers.PrimaryKeyRelatedField(
        queryset=Specialite.objects.all(),
        write_only=True
    )
    matiere = serializers.PrimaryKeyRelatedField(
        queryset=Matiere.objects.all(),
        write_only=True
    )
    specialite_details = SpecialiteSerializer(source='specialite', read_only=True)
    matiere_details = MatiereSerializer(source='matiere', read_only=True)

    class Meta:
        model = CoefficientMatierePhase
        fields = [
            'id_coeffmp',  # ou 'id_coefficient' selon ton modèle
            'coefficient',
            'estPreselection',
            'specialite',         # pour POST (id)
            'matiere',            # pour POST (id)
            'specialite_details', # pour GET (objet)
            'matiere_details'     # pour GET (objet)
        ]

# Adding custom serializers
class CustomNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id_note', 'matiere', 'note', 'est_preselection']

class CustomDiplomeObtenuSerializer(serializers.ModelSerializer):
    notes = CustomNoteSerializer(many=True)

    class Meta:
        model = DiplomeObtenu
        fields = ['id_diplome_obtenu', 'diplome', 'serie', 'pays', 'mention', 'annee', 'notes']

    def create(self, validated_data):
        # Extraire les données des notes
        notes_data = validated_data.pop('notes')

        # Créer le DiplomeObtenu
        diplome_obtenu = DiplomeObtenu.objects.create(**validated_data)

        # Créer les notes associées et les lier au DiplomeObtenu
        notes = [Note.objects.create(**note_data) for note_data in notes_data]
        diplome_obtenu.notes.set(notes)  # Utilisation de .set() pour lier les notes

        return diplome_obtenu
    
class CustomDossierSerializer(serializers.ModelSerializer):
    diplomes_obtenus = CustomDiplomeObtenuSerializer(many=True)

    class Meta:
        model = Dossier
        fields = ['id_dossier', 'specialite', 'date_inscription', 'diplomes_obtenus']

class CustomEleveSerializer(serializers.ModelSerializer):
    dossier = CustomDossierSerializer()

    class Meta:
        model = Eleve
        fields = ['id_eleve', 'nom', 'prenom', 'sexe', 'date_naissance', 'lieu_naissance', 'pays_naissance', 'telephone', 'email', 'addresse', 'dossier']

    def create(self, validated_data):
        dossier_data = validated_data.pop('dossier')
        diplomes_data = dossier_data.pop('diplomes_obtenus')

        # Créer le Dossier sans les diplomes
        dossier = Dossier.objects.create(**dossier_data)

        # Créer les diplomes avec leurs notes via le serializer
        diplomes = []
        for diplome_data in diplomes_data:
            notes_data = diplome_data.pop('notes')
            diplome = DiplomeObtenu.objects.create(**diplome_data)
            notes = [Note.objects.create(**note_data) for note_data in notes_data]
            diplome.notes.set(notes)
            diplomes.append(diplome)

        dossier.diplomes_obtenus.set(diplomes)

        # Créer l'élève
        eleve = Eleve.objects.create(dossier=dossier, **validated_data)
        return eleve
    
class ArchivageSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Jury
    """
    auteur = UtilisateurSerializer(read_only=True)  
    concour = ConcoursSerializer(read_only=True)
    class Meta:
        model = Archivage
        fields = '__all__'  # serialize all the field
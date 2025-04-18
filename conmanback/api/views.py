from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsAdminUser, IsBasicUser
from .models import Profil,Utilisateur, Concours, InfosGenerales, Serie, Mention, Pays, Diplome
from .serializers import (
    ProfilSerializer,UtilisateurSerializer, ConcoursSerializer, InfosGeneralesSerializer, SerieSerializer,
    MentionSerializer, PaysSerializer, DiplomeSerializer, CustomTokenObtainPairViewSerializer
    )

# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Cette vue permet d'obtenir access token et le refresh token et les informations de l'utilisateur
    après avoir reçu l'email et le mot de passe.
    """
    serializer_class = CustomTokenObtainPairViewSerializer


class ProfilViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Profil
    le viewset fournit imédiatement l'opération CRUD sur le modèle profil avec la méthode http adéquates
    Et avec le router dans le fichier urls il génère les endpoints
    """
    queryset = Profil.objects.all() # la source de données que la vue va manipuler
    serializer_class = ProfilSerializer # le serializer qui va être utilisé pour la sérialisation et la désérialisation des données

class UtilisateurViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Utilisateur
    """
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer 

    def get_permissions(self):
        """
        Verifier les permissions avant d'éffectuer les actions
        """
        if self.action in ['create', 'destroy']:
            return [IsAdminUser()]
        elif self.action in ['list', 'retrieve', 'update', 'partial_update']:
            return [IsAdminUser() or IsBasicUser()]
        return [permissions.IsAuthenticated()]

class ConcoursViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Concours
    """
    queryset = Concours.objects.all() 
    serializer_class = ConcoursSerializer
    permission_classes = [permissions.IsAuthenticated]

class InfosGeneralesViewSet(viewsets.ModelViewSet):
    """
    Viewset pour le modèle InfosGenerales
    """
    queryset = InfosGenerales.objects.all()
    serializer_class = InfosGeneralesSerializer
    permission_classes = [permissions.IsAuthenticated]

class SerieViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Serie
    """
    queryset = Serie.objects.all()
    serializer_class = SerieSerializer
    permission_classes = [permissions.IsAuthenticated]

class MentionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Mention
    """
    queryset = Mention.objects.all()
    serializer_class = MentionSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaysViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Pays
    """
    queryset = Pays.objects.all()
    serializer_class = PaysSerializer
    permission_classes = [permissions.IsAuthenticated]

class DiplomeViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Diplome
    """
    queryset = Diplome.objects.all()
    serializer_class = DiplomeSerializer
    permission_classes = [permissions.IsAuthenticated]
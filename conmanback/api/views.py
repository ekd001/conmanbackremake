
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import FileResponse, JsonResponse, HttpResponseNotAllowed
import os
import subprocess
from django.shortcuts import get_object_or_404
from .permissions import IsAdminUser, IsBasicUser
from .models import (Profil,Utilisateur, Concours, InfosGenerales, Serie, Mention, Pays, Diplome, Matiere, Note, DiplomeObtenu, Specialite, 
    Dossier, Eleve, Candidat, Parametre, Jury, MembreJury, CoefficientMatierePhase, Archivage)
from .serializers import (
    ProfilSerializer,UtilisateurSerializer, ConcoursSerializer, InfosGeneralesSerializer, SerieSerializer,
    MentionSerializer, PaysSerializer, DiplomeSerializer, CustomTokenObtainPairViewSerializer, MatiereSerializer, NoteSerializer,
    DiplomeObtenuSerializer, SpecialiteSerializer, DossierSerializer, EleveSerializer, CandidatSerializer, ParametreSerializer, JurySerializer,
    MembreJurySerializer, CoefficientMatierePhaseSerializer
    )

# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Cette vue permet d'obtenir access token et le refresh token et les informations de l'utilisateur
    après avoir reçu l'email et le mot de passe.
    """
    serializer_class = CustomTokenObtainPairViewSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        data = serializer.validated_data
        access = data.pop('access')
        refresh = data.pop('refresh')
        

        response = Response(data, status=status.HTTP_200_OK)

        # Définir les cookies HttpOnly et sécurisés
        response.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=False,              # à activer en production (HTTPS)
            samesite='Lax',
            max_age=60 * 60,          # 60 minutes
            path='/',
            domain='localhost',
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=60 * 60 * 24 * 7,     # 1 jour
            path='/',
            domain='localhost',
        )

        return response

class CurrentUserView(APIView):
    """
    Vue pour obtenir les informations de l'utilisateur actuel
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UtilisateurSerializer(user)
        return Response(serializer.data)

class CustomTokenRefreshView(TokenRefreshView):
    """
    Vue personnalisée pour rafraîchir l'access token avec un refresh token stocké dans un cookie HttpOnly.
    """
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({"message": "Aucun token de rafraîchissement trouvé."}, status=status.HTTP_400_BAD_REQUEST)

        request.data['refresh'] = refresh_token
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')

            # Renvoyer un nouveau cookie access_token
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # à activer en prod
                samesite='Strict',  # ou 'Lax'
                max_age=60 * 60,  # 60 minutes
                path='/',
                domain='localhost',
            )

            response.data = {"message": "Access token mis à jour"}
        
        return response

class ProfilViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Profil
    le viewset fournit imédiatement l'opération CRUD sur le modèle profil avec la méthode http adéquates
    Et avec le router dans le fichier urls il génère les endpoints
    """
    queryset = Profil.objects.all() # la source de données que la vue va manipuler
    serializer_class = ProfilSerializer # le serializer qui va être utilisé pour la sérialisation et la désérialisation des données

class UtilisateurView(APIView):
    """
    ViewSet pour le modèle Utilisateur
    """
    #permissions_classes = [permissions.IsAuthenticated] # verifie qu'il est authentifié
    #serializer_class = UtilisateurSerializer 
    def get(self, request, pk=None):
        """
        Si pk est fourni → retrieve, sinon → list
        """
        if pk:
            user = get_object_or_404(Utilisateur, pk=pk)
            serializer = UtilisateurSerializer(user)
            return Response(serializer.data)
        else:
            users = Utilisateur.objects.all()
            serializer = UtilisateurSerializer(users, many=True)
            return Response(serializer.data)
        

    def post(self, request, *args, **kwargs):
        serializer = UtilisateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        """
        Met à jour complètement un utilisateur
        """
        user = get_object_or_404(Utilisateur, pk=pk)
        serializer = UtilisateurSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Mise à jour partielle
        """
        user = get_object_or_404(Utilisateur, pk=pk)
        serializer = UtilisateurSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Supprime un utilisateur
        """
        user = get_object_or_404(Utilisateur, pk=pk)
        user.delete()
        return Response({"detail": "Utilisateur supprimé."}, status=status.HTTP_204_NO_CONTENT)

  
class ChangerMotDePasseView(APIView):
    """
    Changer le mot de passe d'un utilisateur
    """
    permission_classes = [permissions.IsAuthenticated] # verifie qu'il est authentifié

    def post(self, request, pk):
        user = get_object_or_404(Utilisateur, pk=pk)
        new_password = request.data.get('new_password')

        if not new_password:
            return Response({'detail': 'Mot de passe requis.'}, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(new_password)
        user.save()
        return Response({'detail': 'Mot de passe modifié.'}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    Déconnexion de l'utilisateur : supprime les cookies et blacklist le refresh token.
    """
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({"message": "Aucun token de rafraîchissement trouvé."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Blackliste le refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as e:
            return Response({"message": "Token invalide", "error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # Supprimer les cookies côté client
        response = Response({"message": "Déconnexion réussie"}, status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie('access_token', path='/', domain='localhost')
        response.delete_cookie('refresh_token', path='/', domain='localhost')
        return response
        
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

class MatiereViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Matiere
    """
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer
    permission_classes = [permissions.IsAuthenticated]

class NoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Note
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

class DiplomeObtenuViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle DiplomeObtenu
    """
    queryset = DiplomeObtenu.objects.all()
    serializer_class = DiplomeObtenuSerializer
    permission_classes = [permissions.IsAuthenticated]

class SpecialiteViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Specialite
    """
    queryset = Specialite.objects.all()
    serializer_class = SpecialiteSerializer
    permission_classes = [permissions.IsAuthenticated]

class DossierViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Dossier
    """
    queryset = Dossier.objects.all()
    serializer_class = DossierSerializer
    permission_classes = [permissions.IsAuthenticated]

class EleveViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Eleve
    """
    queryset = Eleve.objects.all()
    serializer_class = EleveSerializer
    permission_classes = [permissions.IsAuthenticated]

class CandidatViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Candidat
    """
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer
    permission_classes = [permissions.IsAuthenticated]

class ParametreViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Parametre
    """
    queryset = Parametre.objects.all()
    serializer_class = ParametreSerializer
    permission_classes = [permissions.IsAuthenticated]

class JuryViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Jury
    """
    queryset = Jury.objects.all()
    serializer_class = JurySerializer
    permission_classes = [permissions.IsAuthenticated]

class MembreJuryViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle MembreJury
    """
    queryset = MembreJury.objects.all()
    serializer_class = MembreJurySerializer
    permission_classes = [permissions.IsAuthenticated]

class CoefficientMatierePhaseViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour le modèle CoefficientMatierePhase
    """
    queryset = CoefficientMatierePhase.objects.all()
    serializer_class = CoefficientMatierePhaseSerializer
    permission_classes = [permissions.IsAuthenticated]


@csrf_exempt
def export_database(request):
    """
    Exporter la base de données au format JSON
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    # Chemin de sortie
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = 'archives'
    export_filename = f"export_{timestamp}.sql"
    export_path = os.path.join(export_dir, export_filename)

    # Crée le dossier s'il n'existe pas
    os.makedirs(export_dir, exist_ok=True)

    try:
        # Export de la base
        with open(export_path, 'w') as f:
            subprocess.run(['sqlite3', 'db.sqlite3', '.dump'], stdout=f, check=True)

        # Enregistre dans le modèle Archivage
        Archivage.objects.create(
            fichier=export_path,
            date=datetime.now()
        )

        # Renvoie le fichier en téléchargement
        return FileResponse(
            open(export_path, 'rb'),
            as_attachment=True,
            filename=export_filename,
            content_type='application/sql'
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

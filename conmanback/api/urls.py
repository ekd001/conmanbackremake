from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    ProfilViewSet,UtilisateurView,ConcoursViewSet, InfosGeneralesViewSet, SerieViewSet, MentionViewSet, PaysViewSet, DiplomeViewSet,
    CustomTokenObtainPairView, LogoutView, ChangerMotDePasseView, MatiereViewSet, NoteViewSet, DiplomeObtenuViewSet, SpecialiteViewSet,
    DossierViewSet, EleveViewSet, CandidatViewSet
)

"""
configuration url pour nos vues
les routes que DefaultRouter() génère : 
/utilisateurs/	GET	liste
/utilisateurs/	POST	création
/utilisateurs/<pk>/	GET	détail
/utilisateurs/<pk>/	PUT	mise à jour
/utilisateurs/<pk>/	PATCH	mise à jour partielle
/utilisateurs/<pk>/	DELETE	suppression
"""
router = DefaultRouter() # Générateur des routes API

router.register(r'profil', ProfilViewSet) # créer les routes CRUD
router.register(r'concours', ConcoursViewSet) 
router.register(r'infos-generales', InfosGeneralesViewSet)
router.register(r'serie', SerieViewSet)
router.register(r'mention', MentionViewSet)
router.register(r'pays', PaysViewSet)
router.register(r'diplome', DiplomeViewSet)
router.register(r'matiere', MatiereViewSet)
router.register(r'note', NoteViewSet)
router.register(r'diplome-obtenu', DiplomeObtenuViewSet)
router.register(r'specialite', SpecialiteViewSet)
router.register(r'dossier', DossierViewSet)
router.register(r'eleve', EleveViewSet)
router.register(r'candidat', CandidatViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('utilisateur/', UtilisateurView.as_view()), # créer 
    path('utilisateur/<int:pk>/', UtilisateurView.as_view()), # récupérer un utilisateur, supprimer ou mettre à jour un utilisateur
    path('login/', CustomTokenObtainPairView.as_view(), name="login"),
    path('changer-mot-de-passe/<int:pk>/', ChangerMotDePasseView.as_view(), name="changer-mot-de-passe"),
    path('token/refresh/',TokenRefreshView.as_view(),name="token-refresh"),
    path('logout/', LogoutView.as_view(), name="logout")
]
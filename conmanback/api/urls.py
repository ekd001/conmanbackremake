from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    ProfilViewSet,UtilisateurViewSet,ConcoursViewSet, InfosGeneralesViewSet, SerieViewSet, MentionViewSet, PaysViewSet, DiplomeViewSet,
    CustomTokenObtainPairView
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
router.register(r'utilisateur', UtilisateurViewSet) 
router.register(r'concours', ConcoursViewSet) 
router.register(r'infos-generales', InfosGeneralesViewSet)
router.register(r'serie', SerieViewSet)
router.register(r'mention', MentionViewSet)
router.register(r'pays', PaysViewSet)
router.register(r'diplome', DiplomeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name="login"),
    path('token/refresh/',TokenRefreshView.as_view(),name="token-refresh")
]
from import_export import resources
from .models import (Concours, Profil, Utilisateur, InfosGenerales, Serie, Mention, 
    Pays, Diplome, Matiere, Note, DiplomeObtenu, Specialite, Dossier, Eleve, Candidat,
    Parametre, Jury, MembreJury, CoefficientMatierePhase
)

class ConcoursResource(resources.ModelResource):

    class Meta:
        model = Concours

class ProfilResource(resources.ModelResource):

    class Meta:
        model = Profil

class UtilisateurResource(resources.ModelResource):

    class Meta:
        model = Utilisateur

class InfosGeneralesResource(resources.ModelResource):

    class Meta:
        model = InfosGenerales

class SerieResource(resources.ModelResource):

    class Meta:
        model = Serie

class MentionResource(resources.ModelResource):

    class Meta:
        model = Mention

class PaysResource(resources.ModelResource):

    class Meta:
        model = Pays

class DiplomeResource(resources.ModelResource):

    class Meta:
        model = Diplome

class MatiereResource(resources.ModelResource):

    class Meta:
        model = Matiere

class NoteResource(resources.ModelResource):

    class Meta:
        model = Note

class SpecialiteResource(resources.ModelResource):

    class Meta:
        model = Specialite

class DossierResource(resources.ModelResource):

    class Meta:
        model = Dossier

class DiplomeObtenuResource(resources.ModelResource):

    class Meta:
        model = DiplomeObtenu

class EleveResource(resources.ModelResource):

    class Meta:
        model = Eleve

class CandidatResource(resources.ModelResource):

    class Meta:
        model = Candidat

class ParametreResource(resources.ModelResource):

    class Meta:
        model = Parametre

class JuryResource(resources.ModelResource):

    class Meta:
        model = Jury

class MembreJuryResource(resources.ModelResource):

    class Meta:
        model = MembreJury

class CoefficientMatierePhaseResource(resources.ModelResource):

    class Meta:
        model = CoefficientMatierePhase

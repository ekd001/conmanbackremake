import os
import django
import sys
# Ajouter le chemin du projet au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurer les paramètres Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conmanback.settings')  # Remplacez 'votre_projet.settings' par le chemin vers votre fichier settings.py
django.setup()

from api.models import (Profil,Utilisateur, Concours, InfosGenerales, Serie, Mention, Pays, Diplome, Matiere, Note, DiplomeObtenu, Specialite, 
    Dossier, Eleve, Parametre, Jury, MembreJury, CoefficientMatierePhase, Archivage, Candidat,)
from api.mocks_data import *

def get_eleves_par_specialite():
    specialites = Specialite.objects.all()
    eleves_par_specialite = {}

    for specialite in specialites:
        eleves = Eleve.objects.filter(dossier__specialite=specialite)
        eleves_par_specialite[specialite] = eleves

    return eleves_par_specialite

def get_coeff_par_specialite(specialite: str):
    return CoefficientMatierePhase.objects.filter(specialite=specialite, )

def calculer_moyenne():
    eleves_par_specialite = get_eleves_par_specialite()
    for specialite, eleves in eleves_par_specialite.items():
        coeff_matiere = get_coeff_par_specialite(specialite)
        for eleve in eleves:
            diplomes_obt = eleve.dossier.diplomes_obtenus
            for e in diplomes_obt:
                if e.diplome.libelle == "":
                    pass
            # Calculer la moyenne de l'eleve
            pass

def main():
    # pays_mock() # Insert Mock Data for Pays entity
    # serie_mock() # Insert Mock Data for Pays entity
    # mention_mock()
    # matiere_mock()
    # specialite_mock()
    # parametre_mock()
    # jury_mock()
    # membre_jury_mock()
    # coefficient_matiere_phase_mock()
    # diplome_mock()
    # eleve_mock()
    dict = get_eleves_par_specialite()
    for e in dict:
        print("*"*50)
        print(f"Specialite -> {e.libelle}")
        for eleve in dict[e]:
            print(f"{eleve.nom}, {eleve.prenom}")

if __name__ == '__main__':
    main()

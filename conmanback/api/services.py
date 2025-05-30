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
from api.mocks_data import run_mock

def get_eleves_par_specialite():
    specialites = Specialite.objects.all()
    eleves_par_specialite = {}

    for specialite in specialites:
        eleves = Eleve.objects.filter(dossier__specialite=specialite)
        eleves_par_specialite[specialite] = eleves

    return eleves_par_specialite

def get_coeff_par_specialite(specialite: str):
    return CoefficientMatierePhase.objects.filter(specialite=specialite, )

def compute_average(notes, coeffs_matieres):
    if not notes:
        print("This eleve has not notes. Returning 0...")
        return 0 
    s = 0
    coeff_sum = 0
    for note in notes:
        print("Interating through notes")
        for coeff_matiere in coeffs_matieres:
            print("Interating through CoefficientMatierePhase")
            if note.matiere == coeff_matiere.matiere:
                s += note.note * coeff_matiere.coefficient
                coeff_sum += coeff_matiere.coefficient
                break
    return s / coeff_sum

def compute_eleve_average(eleve: Eleve, matieres, diploma_to_consider="BAC1"):
    diplomes_obtenus: list[DiplomeObtenu] = eleve.dossier.diplomes_obtenus.all()
    for diplome_obtenu in diplomes_obtenus:
        if diplome_obtenu.diplome.libelle == diploma_to_consider:
            notes = diplome_obtenu.notes.all()
            avg = compute_average(notes, matieres)
            print(f"Eleve -> , {eleve.nom}, {eleve.prenom}, Average -> {avg}")

def calculer_moyenne():
    eleves_par_specialite = get_eleves_par_specialite()
    for specialite, eleves in eleves_par_specialite.items():
        print("Specialite -> ", specialite.libelle)
        coeff_matieres = get_coeff_par_specialite(specialite)
        # print(coeff_matieres)
        for eleve in eleves:
            compute_eleve_average(eleve, coeff_matieres)
            # diplomes_obt = eleve.dossier.diplomes_obtenus
            # for e in diplomes_obt:
            #     if e.diplome.libelle == "":
            #         pass
            # # Calculer la moyenne de l'eleve
            # pass

def main():

    # run_mock ()
    # # Print Eleve objetc per speciality
    # dict = get_eleves_par_specialite()
    # for e in dict:
    #     print("*"*50)
    #     print(f"Specialite -> {e.libelle}")
    #     for eleve in dict[e]:
    #         print(f"{eleve.nom}, {eleve.prenom}")
    calculer_moyenne()

if __name__ == '__main__':
    main()

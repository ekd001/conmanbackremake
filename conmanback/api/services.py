import os
import django
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurer les paramètres Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conmanback.settings')  # Remplacez 'votre_projet.settings' par le chemin vers votre fichier settings.py
django.setup()

from api.models import (Profil,Utilisateur, Concours, InfosGenerales, Serie, Mention, Pays, Diplome, Matiere, Note, DiplomeObtenu, Specialite, 
    Dossier, Eleve, Parametre, Jury, MembreJury, CoefficientMatierePhase, Archivage, Candidat,)
# from api.mocks_data import run_mock
from datetime import date
from api.consts import BAC1_LIBELLE, BAC2_LIBELLE, PHASE_PRESELECTION
from datetime import datetime
import subprocess

def get_eleves_par_specialite():
    specialites = Specialite.objects.all()
    eleves_par_specialite = {}

    for specialite in specialites:
        eleves = Eleve.objects.filter(dossier__specialite=specialite)
        eleves_par_specialite[specialite] = eleves

    return eleves_par_specialite

def get_coeff_par_specialite(specialite: str):
    return CoefficientMatierePhase.objects.filter(specialite=specialite, )

def calculer_moyenne_eleve(notes, coeffs_matieres):
    if not notes:
        print("This eleve has not notes. Returning 0...")
        return 0 
    s = 0
    coeff_sum = 0
    for note in notes:
        # print("Interating through notes")
        for coeff_matiere in coeffs_matieres:
            # print("Interating through CoefficientMatierePhase")
            if note.matiere == coeff_matiere.matiere:
                s += note.note * coeff_matiere.coefficient
                coeff_sum += coeff_matiere.coefficient
                break
    return s / coeff_sum

def calculer_poids_eleve(eleve: Eleve, matieres, diploma_to_consider=BAC2_LIBELLE):
    diplomes_obtenus: list[DiplomeObtenu] = eleve.dossier.diplomes_obtenus.all()
    for diplome_obtenu in diplomes_obtenus:
        if diplome_obtenu.diplome.libelle == diploma_to_consider:
            notes = diplome_obtenu.notes.all()
            return calculer_moyenne_eleve(notes, matieres)
    return 0

def poids_redoublement_bac2(annee_obtention_bac1, annee_obtention_bac2):
    if annee_obtention_bac1 > annee_obtention_bac2 or (annee_obtention_bac1 + annee_obtention_bac2) == 0: return 0
    poids = 6 - (annee_obtention_bac2 - annee_obtention_bac1)
    return poids if poids >= 0 else 0

def poids_anciennete_bac2(annee_obtention):
    poids = 5 - (date.today().year - annee_obtention)
    return poids if 5 >= poids >= 0 else 0

def generer_candidats():
    eleves_par_specialite = get_eleves_par_specialite()
    for specialite, eleves in eleves_par_specialite.items():
        # print("Specialite -> ", specialite.libelle)
        num_table = 1
        coeff_matieres = get_coeff_par_specialite(specialite)
        for eleve in eleves:
            eleve.poids = calculer_poids_eleve(eleve, coeff_matieres)
            # print("eleve.poids -> ", eleve.poids)
            annee_bac2 = 0
            annee_bac1 = 0
            for diplome_obtenu in eleve.dossier.diplomes_obtenus.all():
                # print("Iterating through Diplomes Obtenues -> ", diplome_obtenu.diplome.libelle)
                if diplome_obtenu.diplome.libelle == BAC2_LIBELLE:
                    annee_bac2 = diplome_obtenu.annee.year
                    # print("Annee bac 2 -> ", annee_bac2)
                elif diplome_obtenu.diplome.libelle == BAC1_LIBELLE:
                    annee_bac1 = diplome_obtenu.annee.year
                    # print("Annee bac 1 -> ", annee_bac1)
            eleve.poids += poids_anciennete_bac2(annee_bac2)
            eleve.poids += poids_redoublement_bac2(annee_obtention_bac1=annee_bac1, annee_obtention_bac2=annee_bac2)
            # print("Poids definitif -> ", eleve.poids)
            eleve.save()
            # Mettre ici toute autre logique de sélection pour augmenter ou diminuer le poids d'un élève
            if eleve.poids >= 10:
                # Générer un candidat avec son numéro de table
                candidat = Candidat.objects.create(
                    eleve=eleve,
                    num_table=str(num_table).zfill(3),
                )
                # candidat.save()
                num_table += 1
                print("Candidat créer !")

def get_candidats_specialite(specialite):
    return Candidat.objects.filter(eleve__dossier__specialite__libelle=specialite)

def get_matiere_par_specialite(specialite):
    return CoefficientMatierePhase.objects.filter(estPreselection=Parametre.objects.first().phase_actuel == PHASE_PRESELECTION, specialite__libelle=specialite)

def export_database(user):
    if user is None:
        user = Utilisateur.objects.first()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = 'archives'
    export_filename = f"export_{timestamp}.sql"
    export_path = os.path.join(export_dir, export_filename)

    # Crée le dossier s'il n'existe pas
    os.makedirs(export_dir, exist_ok=True)

    # Export de la base
    with open(export_path, 'w') as f:
        subprocess.run(['sqlite3', 'db.sqlite3', '.dump'], stdout=f, check=True)
    
    # Enregistre dans le modèle Archivage
    Archivage.objects.create(
        fichier=export_path,
        date=datetime.now(),
        concour=Concours.objects.first(),
        auteur=user
    )

    return export_path, export_filename

def add_notes_to_candidat(id_candidat, notes):
    try:
        candidat = Candidat.objects.get(id_candidat=id_candidat)
        candidat.notes.set(notes)  # notes est une liste d’instances Note
        candidat.save()
        print(f"Candidat avec l'ID {id_candidat} mis à jour avec succès.")
    except Candidat.DoesNotExist:
        print(f"Aucun candidat trouvé avec l'ID {id_candidat}.")
        
def main():
    # generer_candidats()
    add_notes_to_candidat(1)
    # export_database()
    # print(get_candidats_specialite("Tronc Commun"))
    # print(poids_anciennete_bac2(0))
    # print(poids_redoublement_bac2(0, 0))

if __name__ == '__main__':
    main()

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
from random import randint

def get_eleves_par_specialite():
    specialites = Specialite.objects.all()
    eleves_par_specialite = {}

    for specialite in specialites:
        eleves = Eleve.objects.filter(dossier__specialite=specialite)
        eleves_par_specialite[specialite] = eleves

    return eleves_par_specialite


def get_candidats_par_specialite():
    specialites = Specialite.objects.all()
    candidats_par_specialite = {}

    for specialite in specialites:
        candidats = Candidat.objects.filter(eleve__dossier__specialite=specialite)
        candidats_par_specialite[specialite] = candidats

    return candidats_par_specialite

def get_coeff_par_specialite(specialite: str, est_preselction=True):
    return CoefficientMatierePhase.objects.filter(specialite=specialite, estPreselection=est_preselction)

def calculer_poids_eleve(eleve: Eleve, matieres, diploma_to_consider=BAC2_LIBELLE):
    diplomes_obtenus: list[DiplomeObtenu] = eleve.dossier.diplomes_obtenus.all()
    for diplome_obtenu in diplomes_obtenus:
        if diplome_obtenu.diplome.libelle == diploma_to_consider:
            notes = diplome_obtenu.notes.all()
            return calculer_moyenne(notes, matieres)
            # return calculer_moyenne_eleve(notes, matieres)
    return 0

def poids_redoublement_bac2(annee_obtention_bac1, annee_obtention_bac2):
    if annee_obtention_bac1 > annee_obtention_bac2 or (annee_obtention_bac1 + annee_obtention_bac2) == 0: return 0
    poids = 6 - (annee_obtention_bac2 - annee_obtention_bac1)
    return poids if poids >= 0 else 0

def poids_anciennete_bac2(annee_obtention):
    poids = 5 - (date.today().year - annee_obtention)
    return poids if 5 >= poids >= 0 else 0

def calculer_moyenne(notes: list[Note], coeff_matieres: list[CoefficientMatierePhase]):
    if not notes:
        print("This eleve has not notes. Returning 0...")
        return 0 
    s = 0
    coeff_sum = 0
    for coeff_matiere in coeff_matieres:
        coeff_sum += coeff_matiere.coefficient
        for note in notes:
            if note.matiere.id_matiere == coeff_matiere.matiere.id_matiere:
                s += note.note * coeff_matiere.coefficient
                break
    return s / coeff_sum

def deliberer_phase_ecrite(moyenne_min=10):
    candidats_par_specialite = get_candidats_par_specialite()
    for specialite, candidats in candidats_par_specialite.items():
        # print("Specialite -> ", specialite.libelle)
        # num_table = 1
        coeff_matieres = get_coeff_par_specialite(specialite, est_preselction=False)
        for candidat in candidats:
            candidat.moyenne = calculer_moyenne(candidat.notes.all(), coeff_matieres)
            print("Moyenne calculé ! ", candidat.eleve.nom, " -> ", candidat.moyenne)
            candidat.reussite = candidat.moyenne >= moyenne_min # Penser à parametre cette valeur
            candidat.save()

def generer_candidats(poids_min=10):
    eleves_par_specialite = get_eleves_par_specialite()
    for specialite, eleves in eleves_par_specialite.items():
        # print("Specialite -> ", specialite.libelle)
        num_table = 1
        coeff_matieres = get_coeff_par_specialite(specialite, est_preselction=True)
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
            if eleve.poids >= poids_min:
                # Générer un candidat avec son numéro de table
                candidat = Candidat.objects.create(
                    eleve=eleve,
                    num_table=str(num_table).zfill(3),
                )
                # candidat.save()
                num_table += 1
                print("Candidat créer !")

def get_candidats_specialite(pk):
    return Candidat.objects.filter(eleve__dossier__specialite__id_specialite=pk)

# def get_candidats_selectionne(specialite):
#     return Candidat.objects.filter(reussite=True)

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
    # print("Time -> ", datetime.now())

    return export_path, export_filename

def a_toutes_les_notes(notes, specialite):
    cmps = get_matiere_par_specialite(specialite)
    for cmp in cmps:
        finded = False
        for note in notes:
            if note.matiere == cmp.matiere:
                finded = True
                break
        if not finded:
            return False
    return True

def add_notes_to_candidat(id_candidat, notes):
    try:
        candidat = Candidat.objects.get(id_candidat=id_candidat)
        candidat.notes.set(notes)  # notes est une liste d’instances Note
        candidat.a_toutes_les_notes = a_toutes_les_notes(notes, candidat.eleve.dossier.specialite)
        candidat.save()
    except Candidat.DoesNotExist:
        print(f"Aucun candidat trouvé avec l'ID {id_candidat}.")

def candidats_notes_mock():
    candidats = Candidat.objects.all()
    for candidat in candidats:
        coeff_mats = CoefficientMatierePhase.objects.filter(specialite=candidat.eleve.dossier.specialite)
        for coeff_mat in coeff_mats:
            candidat.notes.add(
                Note.objects.create(matiere=coeff_mat.matiere, note=randint(8, 19), est_preselection=False),
            )
        
def main():
    generer_candidats(10)
    candidats_notes_mock()
    deliberer_phase_ecrite(8)
    # add_notes_to_candidat(1)
    # export_database()
    # print(get_candidats_specialite("Tronc Commun"))
    # print(poids_anciennete_bac2(0))
    # print(poids_redoublement_bac2(0, 0))

if __name__ == '__main__':
    main()

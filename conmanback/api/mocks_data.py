import os
import django
import sys
# Ajouter le chemin du projet au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurer les paramètres Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conmanback.settings')  # Remplacez 'votre_projet.settings' par le chemin vers votre fichier settings.py
django.setup()

from api.models import (Profil, Utilisateur, Concours, InfosGenerales, Serie, Mention, Pays, Diplome, Matiere, Note, DiplomeObtenu, Specialite, 
    Dossier, Eleve, Parametre, Jury, MembreJury, CoefficientMatierePhase, Archivage, Candidat, Fonctionnalite,)
from faker import Faker
from datetime import date
from random import randint, choice
from api.consts import *
from api.services import export_database

fake = Faker()

def concours_mock():
    Concours.objects.create(
        date_debut=fake.date_between(start_date="-6w", end_date="today"),
        date_fin=fake.date_between(start_date="today", end_date="+6w"),
        annee_civile=str(fake.date_between(start_date="today", end_date="+6w").year),
    )
    print("Concours créer avec succès")

def infos_generales_mock():
    InfosGenerales.objects.create(
        nom_universite="Université de Lomé",
        nom_ecole="Ecole Supérieur des Assistants Administratifs",
        ville=fake.city(),
        rue=fake.street_name(),
        bp=fake.postcode(),
        tel=fake.phone_number(),
        fax=fake.phone_number(),
        email=fake.email(),
        adr_site_web=fake.url(),
        nom_responsable_ecole=fake.name(),
        titre_responsable_ecole=fake.job(),
        nom_responsable_etude=fake.name(),
        titre_responsable_etude=fake.job()
    )
    print("Les informations générales ont été ajoutées avec succès.")

def profil_mock():
    profils_data = [
        {"numProfil": "1", "nomProfil": Profil.ADMIN},
        {"numProfil": "2", "nomProfil": Profil.UTILISATEUR},
    ]

    for profil_data in profils_data:
        Profil.objects.get_or_create(
            numProfil=profil_data["numProfil"],
            nomProfil=profil_data["nomProfil"]
        )
    print("Les profils ont été ajoutés avec succès.")

def utilisateur_mock():
    # Vérifiez que les profils existent
    admin_profil = Profil.objects.filter(nomProfil=Profil.ADMIN).first()
    utilisateur_profil = Profil.objects.filter(nomProfil=Profil.UTILISATEUR).first()

    if not admin_profil or not utilisateur_profil:
        print("Veuillez d'abord exécuter profil_mock pour créer les profils.")
        return

    utilisateurs_data = [
        {"nom": fake.last_name(), "prenom": fake.first_name(), "email": fake.email(), "telephone": fake.phone_number(), "code_access": "admin123", "password": "adminpass", "profil": admin_profil},
        {"nom": fake.last_name(), "prenom": fake.first_name(), "email": fake.email(), "telephone": fake.phone_number(), "code_access": "user123", "password": "userpass", "profil": utilisateur_profil},
    ]

    for utilisateur_data in utilisateurs_data:
        # Vérifiez si l'utilisateur existe déjà
        if not Utilisateur.objects.filter(code_access=utilisateur_data["code_access"]).exists():
            # Créez l'utilisateur en utilisant le manager pour hasher le mot de passe
            Utilisateur.objects.create_user(
                nom=utilisateur_data["nom"],
                prenom=utilisateur_data["prenom"],
                email=utilisateur_data["email"],
                telephone=utilisateur_data["telephone"],
                code_access=utilisateur_data["code_access"],
                password=utilisateur_data["password"],
                profil=utilisateur_data["profil"]
            )
    print("Les utilisateurs ont été ajoutés avec succès.")
    print("Admin : Username -> ",utilisateurs_data[0]["code_access"], "; Password -> ", utilisateurs_data[0]["password"])
    print("Utilisateur Simple : Username -> ",utilisateurs_data[1]["code_access"], "; Password -> ", utilisateurs_data[1]["password"])

def pays_mock():
    pays_data = [
        {"nom_pays": "Togo", "code_pays": "TG", "nationalite": "Togolaise", "indicatif": "+228"},
        {"nom_pays": "France", "code_pays": "FR", "nationalite": "Française", "indicatif": "+33"},
        {"nom_pays": "États-Unis", "code_pays": "US", "nationalite": "Américaine", "indicatif": "+1"},
        {"nom_pays": "Canada", "code_pays": "CA", "nationalite": "Canadienne", "indicatif": "+1"},
        {"nom_pays": "Allemagne", "code_pays": "DE", "nationalite": "Allemande", "indicatif": "+49"},
        {"nom_pays": "Royaume-Uni", "code_pays": "GB", "nationalite": "Britannique", "indicatif": "+44"},
        {"nom_pays": "Italie", "code_pays": "IT", "nationalite": "Italienne", "indicatif": "+39"},
        {"nom_pays": "Espagne", "code_pays": "ES", "nationalite": "Espagnole", "indicatif": "+34"},
        {"nom_pays": "Brésil", "code_pays": "BR", "nationalite": "Brésilienne", "indicatif": "+55"},
        {"nom_pays": "Japon", "code_pays": "JP", "nationalite": "Japonaise", "indicatif": "+81"},
        {"nom_pays": "Chine", "code_pays": "CN", "nationalite": "Chinoise", "indicatif": "+86"},
        {"nom_pays": "Inde", "code_pays": "IN", "nationalite": "Indienne", "indicatif": "+91"},
        {"nom_pays": "Australie", "code_pays": "AU", "nationalite": "Australienne", "indicatif": "+61"},
        {"nom_pays": "Russie", "code_pays": "RU", "nationalite": "Russe", "indicatif": "+7"},
        {"nom_pays": "Mexique", "code_pays": "MX", "nationalite": "Mexicaine", "indicatif": "+52"},
        {"nom_pays": "Afrique du Sud", "code_pays": "ZA", "nationalite": "Sud-Africaine", "indicatif": "+27"},
        {"nom_pays": "Argentine", "code_pays": "AR", "nationalite": "Argentine", "indicatif": "+54"},
        {"nom_pays": "Corée du Sud", "code_pays": "KR", "nationalite": "Sud-Coréenne", "indicatif": "+82"},
        {"nom_pays": "Nigeria", "code_pays": "NG", "nationalite": "Nigériane", "indicatif": "+234"},
        {"nom_pays": "Égypte", "code_pays": "EG", "nationalite": "Égyptienne", "indicatif": "+20"},
        {"nom_pays": "Kenya", "code_pays": "KE", "nationalite": "Kényane", "indicatif": "+254"},
    ]

    for pays in pays_data:
        Pays.objects.get_or_create(
            nom_pays=pays["nom_pays"],
            code_pays=pays["code_pays"],
            nationalite=pays["nationalite"],
            indicatif=pays["indicatif"]
        )
    print("Les pays ont été ajoutés avec succès.")

def serie_mock():
    series_data = [
        {"code":"A1","libelle":"Lettres-mathématiques","points":"25","lstModel":"2"},
        {"code":"A2","libelle":"Lettres-langues","points":"25","lstModel":"2"},
        {"code":"A3","libelle":"Lettre-Arts","points":"25","lstModel":"2"},
        {"code":"A4","libelle":"Langues-mathématiques","points":"25","lstModel":"2"},
        {"code":"A5","libelle":"Langues","points":"25","lstModel":"2"},
        {"code":"B","libelle":"Economique et social","points":"25","lstModel":""},
        {"code":"BG","libelle":"BG","points":"10","lstModel":""},
        {"code":"BTC","libelle":"Brevet de technicien C","points":"10","lstModel":""},
        {"code":"BTG","libelle":"Brevet de technicien G","points":"10","lstModel":""},
        {"code":"BTM","libelle":"Brevet de technicien M","points":"10","lstModel":""},
        {"code":"C","libelle":"Mathématiques et sciences physiques","points":"10","lstModel":"1"},
        {"code":"D","libelle":"Mathématiques et sciences de la nature","points":"10","lstModel":"1"},
        {"code":"E","libelle":"Mathématiques et techniques","points":"10","lstModel":"1"},
        {"code":"F1","libelle":"Construction mécanique","points":"10","lstModel":"1"},
        {"code":"F2","libelle":"Electronique","points":"10","lstModel":"1"},
        {"code":"F3","libelle":"Electrotechnique","points":"10","lstModel":"1"},
        {"code":"F4","libelle":"Génie civil","points":"10","lstModel":""},
        {"code":"G1","libelle":"Techniques administratives","points":"25","lstModel":"2"},
        {"code":"G2","libelle":"Techniques quantitatives de gestion","points":"10","lstModel":""},
        {"code":"G3","libelle":"Techniques commerciales","points":"10","lstModel":""},
        {"code":"S","libelle":"Scientifique - Sciences de l'ingénieur","points":"10","lstModel":""},
        {"code":"Ti","libelle":"Techniques industruelles","points":"10","lstModel":"1"}
    ]

    for serie in series_data:
        Serie.objects.get_or_create(libelle=serie["libelle"], code=serie["code"])
    print("Les séries ont été ajoutées avec succès.")


def mention_mock():
    mentions_data = [
        {"libelle": "Honorable", "abreviation": "HOR", "moy_min": 20.00, "moy_max": 20.00},
        {"libelle": "Excellent", "abreviation": "EX", "moy_min": 18.00, "moy_max": 20.00},
        {"libelle": "Très Bien", "abreviation": "TB", "moy_min": 16.00, "moy_max": 17.99},
        {"libelle": "Bien", "abreviation": "B", "moy_min": 14.00, "moy_max": 15.99},
        {"libelle": "Assez Bien", "abreviation": "AB", "moy_min": 12.00, "moy_max": 13.99},
        {"libelle": "Passable", "abreviation": "P", "moy_min": 10.00, "moy_max": 11.99},
        {"libelle": "Insuffisant", "abreviation": "INSUF", "moy_min": 08.00, "moy_max": 09.99},
        {"libelle": "Très Insuffisant", "abreviation": "TI", "moy_min": 00.00, "moy_max": 07.99},
    ]

    for mention in mentions_data:
        Mention.objects.get_or_create(
            libelle=mention["libelle"],
            abreviation=mention["abreviation"],
            moy_min=mention["moy_min"],
            moy_max=mention["moy_max"]
        )
    print("Les mentions ont été ajoutées avec succès.")

def matiere_mock():
    matieres_data = [
        {"nuMat":"10","libelle":"Mathématiques","abreviation":"MTH","dmnsn":"null"},
        {"nuMat":"20","libelle":"Physiques","abreviation":"PHY","dmnsn":"null"},
        {"nuMat":"30","libelle":"Français","abreviation":"FR","dmnsn":"*"},
        {"nuMat":"33","libelle":"Culture générale","abreviation":"CG","dmnsn":"null"},
        {"nuMat":"40","libelle":"Anglais","abreviation":"ANG","dmnsn":"1"},
        {"nuMat":"50","libelle":"3e langue\/Étude de cas","abreviation":"3L_EC","dmnsn":"1"},
        {"nuMat":"60","libelle":"Tests Pyschotechniques","abreviation":"TPsych","dmnsn":"2"},
        {"nuMat":"91","libelle":"Bac 1 dans le dossier","abreviation":"SsBac1","dmnsn":"1"},
        {"nuMat":"93","libelle":"Etudes Universitaires","abreviation":"ETUNIV","dmnsn":"0"}
    ]

    for matiere in matieres_data:
        Matiere.objects.get_or_create(
            libelle=matiere["libelle"],
            abreviation=matiere["abreviation"]
        )
    print("Les matières ont été ajoutées avec succès.")

def specialite_mock():
    specialites_data = [
        {"libelle": "Tronc Commun", "abreviation": "TCC"},
        {"libelle": "Administration et Gestion", "abreviation": "AG"},
    ]

    for specialite in specialites_data:
        Specialite.objects.get_or_create(
            libelle=specialite["libelle"],
            abreviation=specialite["abreviation"]
        )
    print("Les spécialités ont été ajoutées avec succès.")

def parametre_mock():
    parametres_data = [
        {"duree_max_oisivete": 3600, "bonus_annee_bac": 2, "phase_actuel": PHASE_PRESELECTION},
    ]

    for parametre in parametres_data:
        Parametre.objects.get_or_create(
            duree_max_oisivete=parametre["duree_max_oisivete"],
            bonus_annee_bac=parametre["bonus_annee_bac"],
            phase_actuel=parametre["phase_actuel"],
        )
    print("Les paramètres ont été ajoutés avec succès.")

def jury_mock():
    jurys_data = [
        {"libelle": "Jury Administrative"},
    ]

    for jury in jurys_data:
        Jury.objects.get_or_create(
            libelle=jury["libelle"]
        )
    print("Les jurys ont été ajoutés avec succès.")

def membre_jury_mock():
    jury = Jury.objects.first()  # Assurez-vous qu'au moins un jury existe
    if not jury:
        print("Veuillez d'abord exécuter jury_mock pour créer des jurys.")
        return

    membres_data = [
        {"jury": jury, "nom": "Dupont", "prenom": "Jean"},
        {"jury": jury, "nom": "Martin", "prenom": "Claire"},
        {"jury": jury, "nom": "Durand", "prenom": "Paul"},
    ]

    for membre in membres_data:
        MembreJury.objects.get_or_create(
            jury=membre["jury"],
            nom=membre["nom"],
            prenom=membre["prenom"]
        )
    print("Les membres de jury ont été ajoutés avec succès.")

def coefficient_matiere_phase_mock():
    specialites = Specialite.objects.all()  # Assurez-vous qu'au moins une spécialité existe
    matieres = Matiere.objects.all()  # Assurez-vous qu'au moins une matière existe
    if not specialites or not matieres:
        print("Veuillez d'abord exécuter specialite_mock et matiere_mock pour créer des spécialités et des matières.")
        return

    coefficients_data = []
    # coefficients_data = [
    #     {"specialite": specialite, "matiere": matiere, "estPreselection": True, "coefficient": 5},
    #     {"specialite": specialite, "matiere": matiere, "estPreselection": False, "coefficient": 3},
    # ]
    for specialite in specialites:
        for matiere in matieres:
            coeff = randint(2, 6)
            coefficients_data.append({"specialite": specialite, "matiere": matiere, "estPreselection": False, "coefficient": coeff},)
            coefficients_data.append({"specialite": specialite, "matiere": matiere, "estPreselection": True, "coefficient": coeff},)

    for coeff in coefficients_data:
        CoefficientMatierePhase.objects.get_or_create(
            specialite=coeff["specialite"],
            matiere=coeff["matiere"],
            estPreselection=coeff["estPreselection"],
            coefficient=coeff["coefficient"]
        )
    print("Les coefficients matière phase ont été ajoutés avec succès.")

def diplome_mock():
    diplomes_data = [
        {"libelle": "Certificat d'Etude du Premier Degré", "abreviation": "CEPD"},
        {"libelle": "Brevet d'Etude du Premier Cycle", "abreviation": "BEPC"},
        {"libelle": BAC1_LIBELLE, "abreviation": "BAC 1"},
        {"libelle": BAC2_LIBELLE, "abreviation": "BAC 2"},
        {"libelle": "Brevet de Technicien Supérieur", "abreviation": "BTS"},
        {"libelle": "DUT", "abreviation": "DUT"},
        {"libelle": "Licence", "abreviation": "Licence"},
        {"libelle": "Maîtrise", "abreviation": "Maîtrise"},
        {"libelle": "Ingénieur", "abreviation": "Ingénieur"},
    ]

    for diplome in diplomes_data:
        Diplome.objects.get_or_create(
            libelle=diplome["libelle"],
            abreviation=diplome["abreviation"]
        )
    print("Les diplômes ont été ajoutés avec succès.")

def fonctionnalite_mock():
    fonctionnalite_data = [
        {"libelle": FONCTIONNALITE_DASHBOARD},
        {"libelle": FONCTIONNALITE_CONFIGURATIONS},
        {"libelle": FONCTIONNALITE_UTILISATEURS},
        {"libelle": FONCTIONNALITE_SAISIE},
        {"libelle": FONCTIONNALITE_TRAITEMENTS},
        {"libelle": FONCTIONNALITE_RESULTATS},
        {"libelle": FONCTIONNALITE_ARCHIVES},
    ]

    for diplome in fonctionnalite_data:
        Fonctionnalite.objects.get_or_create(
            libelle=diplome["libelle"]
        )
    print("Les fonctionnalite ont été ajoutés avec succès.")

def eleve_mock():
    specialites = Specialite.objects.all()
    pays = Pays.objects.all()
    # diplomes = Diplome.objects.all()
    series = Serie.objects.all()
    mentions = Mention.objects.all()

    bac2_diplome = Diplome.objects.get(libelle=BAC2_LIBELLE)
    bac1_diplome = Diplome.objects.get(libelle=BAC1_LIBELLE)
    # for diplome in diplomes:
    #     if diplome.libelle == BAC2_LIBELLE:
    #         bac2_diplome = diplome


    if not (specialites.exists() and pays.exists() and series.exists() and mentions.exists()):
        print("Veuillez d'abord exécuter les mocks pour Specialite, Pays, Diplome, Serie et Mention.")
        return

    for _ in range(100):  # Créer 10 élèves
        
        # Créer deux DiplomeObtenus uniques pour chaque élève
        diplome_obtenu_1 = DiplomeObtenu.objects.create(
            diplome=bac1_diplome,
            serie=choice(series),
            pays=choice(pays),
            mention=choice(mentions),
            annee=fake.date_between(start_date="-10y", end_date="today")
        )
        diplome_obtenu_1.notes.add(
            Note.objects.create(matiere=Matiere.objects.filter(libelle="Français").first(), note=randint(8, 16), est_preselection=True), 
            Note.objects.create(matiere=Matiere.objects.filter(libelle="Anglais").first(), note=randint(8, 19), est_preselection=True),
        )

        diplome_obtenu_2 = DiplomeObtenu.objects.create(
            diplome=bac2_diplome,
            serie=diplome_obtenu_1.serie if randint(0, 10) else choice(series),
            pays=diplome_obtenu_1.pays if randint(0, 10) else choice(pays),
            mention=choice(mentions),
            annee=fake.date_between(start_date="-10y", end_date="today")
        )
        diplome_obtenu_2.notes.add(
            Note.objects.create(matiere=Matiere.objects.filter(libelle="Français").first(), note=randint(8, 16), est_preselection=True), 
            Note.objects.create(matiere=Matiere.objects.filter(libelle="Anglais").first(), note=randint(8, 19), est_preselection=True),
        )

        # diplome_obtenu_3 = DiplomeObtenu.objects.create(
        #     diplome=choice(diplomes),
        #     # diplome=bac2_diplome,
        #     serie=choice(series),
        #     pays=choice(pays),
        #     mention=choice(mentions),
        #     annee=fake.date_between(start_date="-10y", end_date="today")
        # )
        specialite = choice(specialites)
        # coeff_mats = CoefficientMatierePhase.objects.filter(specialite=specialite)
        # for coeff_mat in coeff_mats:
        #     diplome_obtenu_3.notes.add(Note.objects.create(matiere=coeff_mat.matiere, note=randint(8, 16), est_preselection=True), )
        # diplome_obtenu_3.notes.add(
        #     Note.objects.create(matiere=Matiere.objects.filter(libelle="Français").first(), note=randint(8, 16), est_preselection=True), 
        #     Note.objects.create(matiere=Matiere.objects.filter(libelle="Anglais").first(), note=randint(8, 19), est_preselection=True),
        # )

        # Créer un Dossier unique pour chaque élève
        dossier = Dossier.objects.create(
            specialite=specialite,
            date_inscription=fake.date_between(start_date="-6w", end_date="today")
        )
        dossier.diplomes_obtenus.add(diplome_obtenu_1, diplome_obtenu_2)

        # Créer un Élève unique
        Eleve.objects.create(
            dossier=dossier,
            nom=fake.last_name(),
            prenom=fake.first_name(),
            sexe=choice(['M', 'F']),
            date_naissance=fake.date_of_birth(minimum_age=18, maximum_age=25),
            lieu_naissance=fake.city(),
            pays_naissance=choice(pays),
            telephone=fake.phone_number(),
            email=fake.email(),
            addresse=fake.address()
        )

    # print("50 élèves ont été créés avec succès.")

def run_mock():
    fonctionnalite_mock()
    concours_mock()
    infos_generales_mock()
    profil_mock()
    utilisateur_mock()
    pays_mock() # Insert Mock Data for Pays entity
    serie_mock() # Insert Mock Data for Pays entity
    mention_mock()
    matiere_mock()
    specialite_mock()
    parametre_mock()
    jury_mock()
    membre_jury_mock()
    coefficient_matiere_phase_mock()
    diplome_mock()
    eleve_mock()

def main():
    run_mock()
    # export_database(None)

if __name__ == '__main__':
    main()

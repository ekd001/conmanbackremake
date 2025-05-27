from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import (Profil,Utilisateur, Concours, InfosGenerales, Serie, Mention, Pays, Diplome, Matiere, Note, DiplomeObtenu, Specialite, 
    Dossier, Eleve, Parametre, Jury, MembreJury, CoefficientMatierePhase, Archivage, Candidat,)
from .services import get_eleves_par_specialite

# class ConcoursAPITestCase(APITestCase):
#     def setUp(self):
#         """
#         Cette méthode est exécutée avant chaque test.
#         Ici, nous créons un concours pour les tests.
#         """
        
#         self.concours_data = {
#             'date_debut': '2025-06-01',
#             'date_fin': '2025-06-30',
#             'annee_civile': '2025',
#         }
#         self.concours = Concours.objects.create(**self.concours_data)
#         self.url = '/api/concours/'

#     def test_get_concours(self):
#         """
#         Tester si nous pouvons récupérer la liste des concours via GET.
#         """
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)  # Vérifie qu'on a un concours
#         self.assertEqual(response.data[0]['annee_civile'], '2025')

#     def test_create_concours(self):
#         """
#         Tester si nous pouvons créer un concours via POST.
#         """
#         response = self.client.post(self.url, self.concours_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['annee_civile'], '2025')

#     def test_update_concours(self):
#         """
#         Tester si nous pouvons mettre à jour un concours via PUT.
#         """
#         updated_data = {
#             'date_debut': '2025-07-01',
#             'date_fin': '2025-07-31',
#             'annee_civile': '2025',
#         }
#         response = self.client.put(f'{self.url}{self.concours.id}/', updated_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['date_debut'], '2025-07-01')

#     def test_delete_concours(self):
#         """
#         Tester si nous pouvons supprimer un concours via DELETE.
#         """
#         response = self.client.delete(f'{self.url}{self.concours.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



# class InfosGeneralesAPITestCase(APITestCase):
#     def setUp(self):
#         """
#         Préparation des données avant chaque test.
#         Crée un objet InfosGenerales pour l'utiliser dans les tests.
#         """
#         self.infos_data = {
#             'nom_universite': 'Université de Paris',
#             'nom_ecole': 'École Supérieure de Technologie',
#             'ville': 'Paris',
#             'rue': '10 Rue de Paris',
#             'bp': '12345',
#             'tel': '0123456789',
#             'fax': '0123456789',
#             'email': 'contact@ecoleparis.com',
#             'adr_site_web': 'http://www.ecoleparis.com',
#             'nom_responsable_ecole': 'M. Dupont',
#             'titre_responsable_ecole': 'Directeur',
#             'nom_responsable_etude': 'Mme Martin',
#             'titre_responsable_etude': 'Responsable des études'
#         }
#         self.infos = InfosGenerales.objects.create(**self.infos_data)
#         self.url = '/api/infos-generales/'  # URL de l'API pour InfosGenerales

#     def test_get_infos_generales(self):
#         """
#         Tester la récupération de la liste des informations générales via GET.
#         """
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)  # On s'attend à avoir une entrée
#         self.assertEqual(response.data[0]['nom_ecole'], 'École Supérieure de Technologie')

#     def test_create_infos_generales(self):
#         """
#         Tester la création d'une nouvelle entrée InfosGenerales via POST.
#         """
#         response = self.client.post(self.url, self.infos_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['nom_ecole'], 'École Supérieure de Technologie')

#     def test_update_infos_generales(self):
#         """
#         Tester la mise à jour des informations générales via PUT.
#         """
#         updated_data = {
#             'nom_universite': 'Université de Lyon',
#             'nom_ecole': 'École d\'Ingénierie',
#             'ville': 'Lyon',
#             'rue': '5 Rue de Lyon',
#             'bp': '67890',
#             'tel': '0987654321',
#             'fax': '0987654321',
#             'email': 'contact@ecolelyon.com',
#             'adr_site_web': 'http://www.ecolelyon.com',
#             'nom_responsable_ecole': 'M. Lefevre',
#             'titre_responsable_ecole': 'Directeur général',
#             'nom_responsable_etude': 'Mme Bernard',
#             'titre_responsable_etude': 'Directrice des études'
#         }
#         response = self.client.put(f'{self.url}{self.infos.id}/', updated_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['nom_universite'], 'Université de Lyon')

#     def test_delete_infos_generales(self):
#         """
#         Tester la suppression d'une entrée InfosGenerales via DELETE.
#         """
#         response = self.client.delete(f'{self.url}{self.infos.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# class SerieAPITestCase(APITestCase):
#     def setUp(self):
#         """
#         Prépare les données avant chaque test.
#         Crée une instance de Serie pour l'utiliser dans les tests.
#         """
#         self.serie_data = {
#             'libelle': 'Série A',
#         }
#         self.serie = Serie.objects.create(**self.serie_data)
#         self.url = '/api/serie/'  # L'URL de l'API pour Serie

#     def test_get_serie(self):
#         """
#         Tester la récupération de la liste des séries via GET.
#         """
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)  # On attend une entrée
#         self.assertEqual(response.data[0]['libelle'], 'Série A')

#     def test_create_serie(self):
#         """
#         Tester la création d'une nouvelle série via POST.
#         """
#         response = self.client.post(self.url, self.serie_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['libelle'], 'Série A')

#     def test_update_serie(self):
#         """
#         Tester la mise à jour d'une série via PUT.
#         """
#         updated_data = {
#             'libelle': 'Série B',
#         }
#         response = self.client.put(f'{self.url}{self.serie.id}/', updated_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['libelle'], 'Série B')

#     def test_delete_serie(self):
#         """
#         Tester la suppression d'une série via DELETE.
#         """
#         response = self.client.delete(f'{self.url}{self.serie.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# class GetElevesParSpecialiteTestCase(TestCase):
#     def setUp(self):
#         # Créer des spécialités de test
#         self.specialite1 = Specialite.objects.create(libelle='Génie Logiciel', abreviation="INF")
#         self.specialite2 = Specialite.objects.create(libelle='Systèmes Réseau Informatiques', abreviation="SRI")

#         # Créer des élèves de test
#         Eleve.objects.create(
#             nom="Gossou"
#         )
#         Eleve.objects.create(nom='Bob', specialite=self.specialite1)
#         Eleve.objects.create(nom='Charlie', specialite=self.specialite2)

#     def test_get_eleves_par_specialite(self):
#         # Appeler la fonction à tester
#         result = get_eleves_par_specialite()

#         # Vérifier que le résultat contient les spécialités attendues
#         self.assertIn(self.specialite1, result)
#         self.assertIn(self.specialite2, result)

#         # Vérifier que chaque spécialité a le bon nombre d'élèves
#         self.assertEqual(len(result[self.specialite1]), 2)
#         self.assertEqual(len(result[self.specialite2]), 1)

#         # Vérifier que les élèves sont correctement associés à leurs spécialités
#         self.assertEqual(result[self.specialite1][0].nom, 'Alice')
#         self.assertEqual(result[self.specialite1][1].nom, 'Bob')
#         self.assertEqual(result[self.specialite2][0].nom, 'Charlie')
    
#     def create_eleves():
#         pays = Pays.objects.first()  # Assurez-vous qu'un pays existe dans la base
#         dossier = Dossier.objects.first()  # Assurez-vous qu'un dossier existe dans la base

#         if not pays or not dossier:
#             print("Veuillez créer un pays et un dossier avant d'exécuter ce script.")
#             return

#         eleves_data = [
#             {"nom": "Dupont", "prenom": "Jean", "sexe": "M", "date_naissance": "2005-01-01", "lieu_naissance": "Paris", "telephone": "0102030405", "email": "jean.dupont@example.com", "addresse": "10 rue de Paris"},
#             {"nom": "Martin", "prenom": "Claire", "sexe": "F", "date_naissance": "2006-02-02", "lieu_naissance": "Lyon", "telephone": "0203040506", "email": "claire.martin@example.com", "addresse": "20 rue de Lyon"},
#             {"nom": "Durand", "prenom": "Paul", "sexe": "M", "date_naissance": "2007-03-03", "lieu_naissance": "Marseille", "telephone": "0304050607", "email": "paul.durand@example.com", "addresse": "30 rue de Marseille"},
#             {"nom": "Moreau", "prenom": "Sophie", "sexe": "F", "date_naissance": "2008-04-04", "lieu_naissance": "Toulouse", "telephone": "0405060708", "email": "sophie.moreau@example.com", "addresse": "40 rue de Toulouse"},
#             {"nom": "Lemoine", "prenom": "Luc", "sexe": "M", "date_naissance": "2009-05-05", "lieu_naissance": "Nice", "telephone": "0506070809", "email": "luc.lemoine@example.com", "addresse": "50 rue de Nice"},
#             {"nom": "Roux", "prenom": "Julie", "sexe": "F", "date_naissance": "2010-06-06", "lieu_naissance": "Nantes", "telephone": "0607080910", "email": "julie.roux@example.com", "addresse": "60 rue de Nantes"},
#             {"nom": "Blanc", "prenom": "Pierre", "sexe": "M", "date_naissance": "2011-07-07", "lieu_naissance": "Strasbourg", "telephone": "0708091011", "email": "pierre.blanc@example.com", "addresse": "70 rue de Strasbourg"},
#             {"nom": "Fournier", "prenom": "Emma", "sexe": "F", "date_naissance": "2012-08-08", "lieu_naissance": "Bordeaux", "telephone": "0809101112", "email": "emma.fournier@example.com", "addresse": "80 rue de Bordeaux"},
#             {"nom": "Girard", "prenom": "Louis", "sexe": "M", "date_naissance": "2013-09-09", "lieu_naissance": "Lille", "telephone": "0910111213", "email": "louis.girard@example.com", "addresse": "90 rue de Lille"},
#             {"nom": "Bertrand", "prenom": "Alice", "sexe": "F", "date_naissance": "2014-10-10", "lieu_naissance": "Rennes", "telephone": "1011121314", "email": "alice.bertrand@example.com", "addresse": "100 rue de Rennes"},
#         ]

#         for data in eleves_data:
#             Eleve.objects.create(
#                 dossier=dossier,
#                 pays_naissance=pays,
#                 **data
#             )
#         print("10 élèves ont été créés avec succès.")

class ApplicationTest(TestCase):

    def setUp(self):
        self.pays = Pays.objects.all()
        self.profil = Profil.objects.all()
        self.utilisateurs = Utilisateur.objects.all()
        self.Concours = Concours.objects.all()
        self.infos_generales = InfosGenerales.objects.all()
        self.series = Serie.objects.all()
        self.mentions = Mention.objects.all()
        self.diplomes = Diplome.objects.all()
        self.matieres = Matiere.objects.all()
        self.specialites = Specialite.objects.all()
        self.parametres = Parametre.objects.all()
        self.jurys = Jury.objects.all()
        self.membre_jury = MembreJury.objects.all()
        self.coeff_mat = CoefficientMatierePhase.objects.all()
    
    def objects_infos(self):
        print(f"Pays -> {self.pays}")
        print(f"Taille Pays -> {len(self.pays)}")


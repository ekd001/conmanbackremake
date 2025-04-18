from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Concours, InfosGenerales, Serie

class ConcoursAPITestCase(APITestCase):
    def setUp(self):
        """
        Cette méthode est exécutée avant chaque test.
        Ici, nous créons un concours pour les tests.
        """
        
        self.concours_data = {
            'date_debut': '2025-06-01',
            'date_fin': '2025-06-30',
            'annee_civile': '2025',
        }
        self.concours = Concours.objects.create(**self.concours_data)
        self.url = '/api/concours/'

    def test_get_concours(self):
        """
        Tester si nous pouvons récupérer la liste des concours via GET.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Vérifie qu'on a un concours
        self.assertEqual(response.data[0]['annee_civile'], '2025')

    def test_create_concours(self):
        """
        Tester si nous pouvons créer un concours via POST.
        """
        response = self.client.post(self.url, self.concours_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['annee_civile'], '2025')

    def test_update_concours(self):
        """
        Tester si nous pouvons mettre à jour un concours via PUT.
        """
        updated_data = {
            'date_debut': '2025-07-01',
            'date_fin': '2025-07-31',
            'annee_civile': '2025',
        }
        response = self.client.put(f'{self.url}{self.concours.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['date_debut'], '2025-07-01')

    def test_delete_concours(self):
        """
        Tester si nous pouvons supprimer un concours via DELETE.
        """
        response = self.client.delete(f'{self.url}{self.concours.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class InfosGeneralesAPITestCase(APITestCase):
    def setUp(self):
        """
        Préparation des données avant chaque test.
        Crée un objet InfosGenerales pour l'utiliser dans les tests.
        """
        self.infos_data = {
            'nom_universite': 'Université de Paris',
            'nom_ecole': 'École Supérieure de Technologie',
            'ville': 'Paris',
            'rue': '10 Rue de Paris',
            'bp': '12345',
            'tel': '0123456789',
            'fax': '0123456789',
            'email': 'contact@ecoleparis.com',
            'adr_site_web': 'http://www.ecoleparis.com',
            'nom_responsable_ecole': 'M. Dupont',
            'titre_responsable_ecole': 'Directeur',
            'nom_responsable_etude': 'Mme Martin',
            'titre_responsable_etude': 'Responsable des études'
        }
        self.infos = InfosGenerales.objects.create(**self.infos_data)
        self.url = '/api/infos-generales/'  # URL de l'API pour InfosGenerales

    def test_get_infos_generales(self):
        """
        Tester la récupération de la liste des informations générales via GET.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # On s'attend à avoir une entrée
        self.assertEqual(response.data[0]['nom_ecole'], 'École Supérieure de Technologie')

    def test_create_infos_generales(self):
        """
        Tester la création d'une nouvelle entrée InfosGenerales via POST.
        """
        response = self.client.post(self.url, self.infos_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nom_ecole'], 'École Supérieure de Technologie')

    def test_update_infos_generales(self):
        """
        Tester la mise à jour des informations générales via PUT.
        """
        updated_data = {
            'nom_universite': 'Université de Lyon',
            'nom_ecole': 'École d\'Ingénierie',
            'ville': 'Lyon',
            'rue': '5 Rue de Lyon',
            'bp': '67890',
            'tel': '0987654321',
            'fax': '0987654321',
            'email': 'contact@ecolelyon.com',
            'adr_site_web': 'http://www.ecolelyon.com',
            'nom_responsable_ecole': 'M. Lefevre',
            'titre_responsable_ecole': 'Directeur général',
            'nom_responsable_etude': 'Mme Bernard',
            'titre_responsable_etude': 'Directrice des études'
        }
        response = self.client.put(f'{self.url}{self.infos.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nom_universite'], 'Université de Lyon')

    def test_delete_infos_generales(self):
        """
        Tester la suppression d'une entrée InfosGenerales via DELETE.
        """
        response = self.client.delete(f'{self.url}{self.infos.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SerieAPITestCase(APITestCase):
    def setUp(self):
        """
        Prépare les données avant chaque test.
        Crée une instance de Serie pour l'utiliser dans les tests.
        """
        self.serie_data = {
            'libelle': 'Série A',
        }
        self.serie = Serie.objects.create(**self.serie_data)
        self.url = '/api/serie/'  # L'URL de l'API pour Serie

    def test_get_serie(self):
        """
        Tester la récupération de la liste des séries via GET.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # On attend une entrée
        self.assertEqual(response.data[0]['libelle'], 'Série A')

    def test_create_serie(self):
        """
        Tester la création d'une nouvelle série via POST.
        """
        response = self.client.post(self.url, self.serie_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['libelle'], 'Série A')

    def test_update_serie(self):
        """
        Tester la mise à jour d'une série via PUT.
        """
        updated_data = {
            'libelle': 'Série B',
        }
        response = self.client.put(f'{self.url}{self.serie.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['libelle'], 'Série B')

    def test_delete_serie(self):
        """
        Tester la suppression d'une série via DELETE.
        """
        response = self.client.delete(f'{self.url}{self.serie.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

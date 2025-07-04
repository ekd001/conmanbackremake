from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.forms import ValidationError
from .consts import *

# Create your models here.

class Profil(models.Model):
    """
    modèle représentatnt le profil d'un utilisateur
    """
    # Type énumérateur qui définit les types de profil et qui sont attribué à nomProfil

    ADMIN = 'admin'
    UTILISATEUR = 'utilisateur'
   
    numProfil = models.CharField(max_length=100)
    nomProfil = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nomProfil}"


class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        profil = extra_fields.get('profil')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        # Attribution des fonctionnalités selon le profil
        if profil and hasattr(profil, 'nomProfil'):
            if profil.nomProfil == Profil.ADMIN:
                print("Adding all fonctinnalities to the ADMIN")
                # Admin : toutes les fonctionnalités
                toutes_foncts = Fonctionnalite.objects.all()
                user.fonctionnalites.set(toutes_foncts)
            else:
                # Autres profils : Dashboard, Configurations, Saisie
                dash, _ = Fonctionnalite.objects.get_or_create(libelle=FONCTIONNALITE_DASHBOARD)
                config, _ = Fonctionnalite.objects.get_or_create(libelle=FONCTIONNALITE_CONFIGURATIONS)
                saisie, _ = Fonctionnalite.objects.get_or_create(libelle=FONCTIONNALITE_SAISIE)
                user.fonctionnalites.set([dash, config, saisie])

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class Fonctionnalite(models.Model):
    """
    modèle représentant une Fonctionnalite
    """
    id = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return f"Archive : {self.date}"


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    """
    modèle représentant un utilisateur
    """
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    code_access = models.CharField(max_length=100,unique=True)
    fonctionnalites = models.ManyToManyField(Fonctionnalite, related_name="Utilisateur")  # Many-to-Many relation

    objects = UtilisateurManager()
   
    profil = models.ForeignKey(Profil,on_delete=models.SET_NULL,null=True, related_name="Utilisateur")

    # Tous ce qui suit ne pas se préoccupée quelques configurations pour l'authentification
    USERNAME_FIELD = "code_access"
    REQUIRED_FIELDS = []


     # Ajouter des 'related_name' pour éviter les conflits avec le modèle User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customeruser_set',  # Spécifier un nom unique pour la relation inverse
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customeruser_permissions_set',  # Spécifier un nom unique pour la relation inverse
        blank=True
    )

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
    def est_admin(self):
        """
        Vérifie si l'utilisateur est un administrateur
        """
        return self.profil.nomProfil == Profil.ADMIN
    
    def est_non_admin(self):
        """
        Vérifie si l'utilisateur n'est pas un admin
        """
        return self.profil.nomProfil == Profil.UTILISATEUR 

class Concours(models.Model):
    """
    modèle représentant un concours
    """
    date_debut = models.CharField(max_length=100)
    date_fin = models.CharField(max_length=100)
    annee_civile = models.CharField(max_length=100)

    def __str__(self):
        return f"Concours de l'année {self.annee_civile}"

class InfosGenerales(models.Model):
    """
    modèle représentant les informations générales
    """
    nom_universite = models.CharField(max_length=100)
    nom_ecole = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    rue = models.CharField(max_length=100)
    bp = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    fax = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    adr_site_web = models.CharField(max_length=255)
    nom_responsable_ecole = models.CharField(max_length=100)
    titre_responsable_ecole = models.CharField(max_length=100)
    nom_responsable_etude = models.CharField(max_length=100)
    titre_responsable_etude = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom_ecole} {self.nom_universite}"

class Serie(models.Model):
    """
    modèle représentant une série
    """
    id_serie = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=100)
    code = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f"{self.libelle}"
    
class Mention(models.Model):
    """
    modèle représentant une mention
    """
    id_mention = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=100)
    abreviation = models.CharField(max_length=100)
    moy_min = models.DecimalField(max_digits=4, decimal_places=2) # Dans le diagramme c'est integer or la moy doit être en décimale
    moy_max = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.libelle}"
    
class Pays(models.Model):
    """
    modèle représentant un pays
    """
    id_pays = models.AutoField(primary_key=True) 
    nom_pays = models.CharField(max_length=100) # Chacune des champs de ce model doit etre unique dans la base de donnée
    code_pays = models.CharField(max_length=3)
    nationalite = models.CharField(max_length=100, null=True)
    indicatif = models.CharField(max_length=5, null=True)

    def __str__(self):
        return f"{self.nom_pays}"

class Diplome(models.Model):
    """
    modèle représentant un diplôme
    """
    id_diplome = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=100)
    abreviation = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.libelle}"
    

class Matiere(models.Model):
    """
    modèle représentant une matière
    """
    id_matiere = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=100)
    abreviation = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.libelle}"
    
class Note(models.Model):
    """
    modèle représentant une matière
    """
    id_note = models.AutoField(primary_key=True)
    matiere = models.ForeignKey(Matiere,on_delete=models.SET_NULL,null=True, related_name="Note")
    note = models.DecimalField(max_digits=4, decimal_places=2)
    est_preselection = models.BooleanField(default=True)

    def __str__(self):
        return f"ID MAtiere -> {self.matiere} Note -> {self.note}" 

class Specialite(models.Model):
    """
    modèle représentant une Spécialité 
    """
    id_specialite = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=100)
    abreviation = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.__dict__}"

class Dossier(models.Model):
    """
    Modèle représentant un Dossier
    """
    id_dossier = models.AutoField(primary_key=True)
    specialite = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True, related_name="Dossier")
    diplomes_obtenus = models.ManyToManyField("DiplomeObtenu", related_name="dossiers", blank=True)
    date_inscription = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Dossier ID: {self.id_dossier}, Spécialité: {self.specialite}"

class DiplomeObtenu(models.Model):
    """
    Modèle représentant un diplôme obtenu
    """
    id_diplome_obtenu = models.AutoField(primary_key=True)
    diplome = models.ForeignKey(Diplome, on_delete=models.SET_NULL, null=True, related_name="DiplomeObtenu")
    serie = models.ForeignKey(Serie, on_delete=models.SET_NULL, null=True, related_name="DiplomeObtenu")
    pays = models.ForeignKey(Pays, on_delete=models.SET_NULL, null=True, related_name="DiplomeObtenu")
    mention = models.ForeignKey(Mention, on_delete=models.SET_NULL, null=True, related_name="DiplomeObtenu")
    notes = models.ManyToManyField(Note, related_name="DiplomesObtenus")  # Many-to-Many relation
    annee = models.DateField()

    def __str__(self):
        return f"DiplomeObtenu {self.diplome} ({self.annee})"

class Eleve(models.Model):
    """
    modèle représentant un Eleve
    """
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Feminin'),
    ]

    id_eleve = models.AutoField(primary_key=True)
    dossier = models.ForeignKey(Dossier, on_delete=models.SET_NULL, null=True, related_name="Eleve")  # One-to-Many relation
    nom = models.CharField(max_length=100, null=True)
    prenom = models.CharField(max_length=100, null=True)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, default="M")  # Enumération pour le sexe
    date_naissance = models.DateField(null=True)
    lieu_naissance = models.CharField(max_length=100, null=True)
    pays_naissance = models.ForeignKey(Pays, on_delete=models.SET_NULL, null=True, related_name="Eleve")
    telephone = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    addresse = models.CharField(max_length=100, null=True)
    poids = models.DecimalField(max_digits=6, decimal_places=4, default=0)

    def __str__(self):
        return f"Eleve : {self.nom}, {self.prenom}"

class Candidat(models.Model):  # Ajout de models.Model
    """
    modèle représentant un Candidat
    """
    id_candidat = models.AutoField(primary_key=True)
    num_table = models.CharField(max_length=4, null=True)
    eleve = models.OneToOneField(Eleve, on_delete=models.SET_NULL, null=True, related_name="candidat")  # Relation one-to-one
    notes = models.ManyToManyField(Note, related_name="Candidat")  # Many-to-Many relation
    moyenne = models.DecimalField(max_digits=6, decimal_places=4, default=0)
    reussite = models.BooleanField(default=False)
    a_toutes_les_notes = models.BooleanField(default=False)

    def __str__(self):
        return f"Candidat : {self.num_table}, {self.eleve.nom}"

class Parametre(models.Model):
    """
    modèle représentant un Parametre
    """
    PHASE_CHOICES = [
        ('Préalable', 'préalable'),
        ('Préselection', 'préselection'),
        ('Écrite', 'écrite'),
        ('Terminé', 'terminé'),
    ]
    id_parametre = models.AutoField(primary_key=True)
    duree_max_oisivete = models.IntegerField(null=True)
    bonus_annee_bac = models.IntegerField(null=True)
    phase_actuel = models.CharField(max_length=20, choices=PHASE_CHOICES, default='préalable')

    def save(self, *args, **kwargs):
        if not self.pk and Parametre.objects.exists():
            raise ValidationError("Il ne peut y avoir qu'une seule instance de Parametre.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Oisivete : {self.duree_max_oisivete}, Bonus Annee Bac : {self.bonus_annee_bac}"

    class Meta:
        verbose_name = "Paramètre"
        verbose_name_plural = "Paramètres"

class Jury(models.Model):
    """
    modèle représentant un Jury
    """
    id_jury = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=100)

    def __str__(self):
        return f"Jury : {self.libelle}"

class MembreJury(models.Model):
    """
    modèle représentant un membre de Jury
    """
    id_membre = models.AutoField(primary_key=True)
    jury = models.ForeignKey(Jury, on_delete=models.SET_NULL, null=True, related_name="MembreJury")  # One-to-Many relation
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    def __str__(self):
        return f"Membre Jury : {self.nom}, {self.prenom}"

class CoefficientMatierePhase(models.Model):
    """
    modèle représentant les informations concernant une matiere dans chaque phase
    """
    id_coeffmp = models.AutoField(primary_key=True) # coeffmp -> coeff = coefficient, m = matiere, p = phase
    specialite = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True, related_name="CoeffMP")  # One-to-Many relation
    matiere = models.ForeignKey(Matiere, on_delete=models.SET_NULL, null=True, related_name="CoeffMP")  # One-to-Many relation
    estPreselection = models.BooleanField(default=True)
    coefficient = models.IntegerField(null=True)

    def __str__(self):
        return f"Coefficient Matiere Phase : {self.matiere}, {self.coefficient}. Preselection : {self.estPreselection}"

class Archivage(models.Model):
    """
    modèle représentant un Archive
    """
    id_archive = models.AutoField(primary_key=True)
    fichier = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, related_name="Archive")
    concour = models.ForeignKey(Concours, on_delete=models.SET_NULL, null=True, related_name="Archive") 

    def __str__(self):
        return f"Archive : {self.date}"

# Generated by Django 4.2.20 on 2025-05-19 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archivage',
            fields=[
                ('id_archive', models.AutoField(primary_key=True, serialize=False)),
                ('fichier', models.CharField(max_length=255)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Concours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.CharField(max_length=100)),
                ('date_fin', models.CharField(max_length=100)),
                ('annee_civile', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Diplome',
            fields=[
                ('id_diplome', models.AutoField(primary_key=True, serialize=False)),
                ('libelle', models.CharField(max_length=100)),
                ('abreviation', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DiplomeObtenu',
            fields=[
                ('id_diplome_obtenu', models.AutoField(primary_key=True, serialize=False)),
                ('annee', models.DateField()),
                ('diplome', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='DiplomeObtenu', to='api.diplome')),
            ],
        ),
        migrations.CreateModel(
            name='Dossier',
            fields=[
                ('id_dossier', models.AutoField(primary_key=True, serialize=False)),
                ('date_inscription', models.DateField()),
                ('diplomes_obtenus', models.ManyToManyField(blank=True, related_name='dossiers', to='api.diplomeobtenu')),
            ],
        ),
        migrations.CreateModel(
            name='InfosGenerales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_universite', models.CharField(max_length=100)),
                ('nom_ecole', models.CharField(max_length=100)),
                ('ville', models.CharField(max_length=100)),
                ('rue', models.CharField(max_length=100)),
                ('bp', models.CharField(max_length=100)),
                ('tel', models.CharField(max_length=100)),
                ('fax', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('adr_site_web', models.CharField(max_length=255)),
                ('nom_responsable_ecole', models.CharField(max_length=100)),
                ('titre_responsable_ecole', models.CharField(max_length=100)),
                ('nom_responsable_etude', models.CharField(max_length=100)),
                ('titre_responsable_etude', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Jury',
            fields=[
                ('id_jury', models.AutoField(primary_key=True, serialize=False)),
                ('libelle', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Matiere',
            fields=[
                ('id_matiere', models.AutoField(primary_key=True, serialize=False)),
                ('libelle', models.CharField(max_length=100)),
                ('abreviation', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Mention',
            fields=[
                ('id_mention', models.AutoField(primary_key=True, serialize=False)),
                ('libelle', models.CharField(max_length=100)),
                ('abreviation', models.CharField(max_length=100)),
                ('moy_min', models.DecimalField(decimal_places=2, max_digits=4)),
                ('moy_max', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Parametre',
            fields=[
                ('id_parametre', models.AutoField(primary_key=True, serialize=False)),
                ('duree_max_oisivete', models.IntegerField(null=True)),
                ('bonus_annee_bac', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pays',
            fields=[
                ('id_pays', models.AutoField(primary_key=True, serialize=False)),
                ('nom_pays', models.CharField(max_length=100)),
                ('code_pays', models.CharField(max_length=3)),
                ('nationalite', models.CharField(max_length=100, null=True)),
                ('indicatif', models.CharField(max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numProfil', models.CharField(max_length=100)),
                ('nomProfil', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id_serie', models.AutoField(primary_key=True, serialize=False)),
                ('libelle', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Specialite',
            fields=[
                ('id_specialite', models.AutoField(primary_key=True, serialize=False)),
                ('libelle', models.CharField(max_length=100)),
                ('abreviation', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id_note', models.AutoField(primary_key=True, serialize=False)),
                ('note', models.DecimalField(decimal_places=2, max_digits=4)),
                ('est_preselection', models.BooleanField(default=True)),
                ('matiere', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Note', to='api.matiere')),
            ],
        ),
        migrations.CreateModel(
            name='MembreJury',
            fields=[
                ('id_membre', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('jury', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='MembreJury', to='api.jury')),
            ],
        ),
        migrations.CreateModel(
            name='Eleve',
            fields=[
                ('id_eleve', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100, null=True)),
                ('prenom', models.CharField(max_length=100, null=True)),
                ('sexe', models.CharField(choices=[('M', 'Masculin'), ('F', 'Feminin')], default='M', max_length=1)),
                ('date_naissance', models.DateField(null=True)),
                ('lieu_naissance', models.CharField(max_length=100, null=True)),
                ('telephone', models.CharField(max_length=20, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('addresse', models.CharField(max_length=100, null=True)),
                ('dossier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Eleve', to='api.dossier')),
                ('pays_naissance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Eleve', to='api.pays')),
            ],
        ),
        migrations.AddField(
            model_name='dossier',
            name='specialite',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Dossier', to='api.specialite'),
        ),
        migrations.AddField(
            model_name='diplomeobtenu',
            name='mention',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='DiplomeObtenu', to='api.mention'),
        ),
        migrations.AddField(
            model_name='diplomeobtenu',
            name='notes',
            field=models.ManyToManyField(related_name='DiplomesObtenus', to='api.note'),
        ),
        migrations.AddField(
            model_name='diplomeobtenu',
            name='pays',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='DiplomeObtenu', to='api.pays'),
        ),
        migrations.AddField(
            model_name='diplomeobtenu',
            name='serie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='DiplomeObtenu', to='api.serie'),
        ),
        migrations.CreateModel(
            name='CoefficientMatierePhase',
            fields=[
                ('id_coeffmp', models.AutoField(primary_key=True, serialize=False)),
                ('estPreselection', models.BooleanField(default=True)),
                ('coefficient', models.IntegerField(null=True)),
                ('matiere', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='CoeffMP', to='api.matiere')),
                ('specialite', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='CoeffMP', to='api.specialite')),
            ],
        ),
        migrations.CreateModel(
            name='Candidat',
            fields=[
                ('id_candidat', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('num_table', models.CharField(max_length=4, null=True, unique=True)),
                ('eleve', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='candidat', to='api.eleve')),
                ('notes', models.ManyToManyField(related_name='Candidat', to='api.note')),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=100)),
                ('code_access', models.CharField(max_length=100, unique=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='customeruser_set', to='auth.group')),
                ('profil', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Utilisateur', to='api.profil')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='customeruser_permissions_set', to='auth.permission')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

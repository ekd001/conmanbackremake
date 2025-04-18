# Generated by Django 5.1.7 on 2025-04-18 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='customeruser_set', to='auth.group'),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='customeruser_permissions_set', to='auth.permission'),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='email',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]

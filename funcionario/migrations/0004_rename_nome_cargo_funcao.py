# Generated by Django 5.1.4 on 2024-12-20 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funcionario', '0003_remove_cargo_colaborador'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cargo',
            old_name='nome',
            new_name='funcao',
        ),
    ]

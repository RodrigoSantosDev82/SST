# Generated by Django 5.1.4 on 2024-12-20 12:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionario', '0006_alter_funcionario_cargo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='cargo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='funcionario.cargo'),
        ),
    ]
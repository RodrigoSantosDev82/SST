# Generated by Django 5.1.4 on 2024-12-20 13:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funcionario', '0009_alter_funcionario_cargo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='cargo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='funcionario.cargo'),
            preserve_default=False,
        ),
    ]
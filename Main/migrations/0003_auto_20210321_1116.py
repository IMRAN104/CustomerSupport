# Generated by Django 3.1.7 on 2021-03-21 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_complain_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complain',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Main.complain'),
        ),
    ]
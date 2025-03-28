# Generated by Django 4.2.16 on 2024-12-30 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_recipientaddresses_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipientaddresses',
            name='nickname',
            field=models.CharField(blank=True, help_text="Nickname for this address (e.g., 'Mum and Dad', etc)", max_length=50),
        ),
    ]

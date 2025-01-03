# Generated by Django 3.2.25 on 2024-10-27 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_recipientaddresses_is_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipientaddresses',
            name='nickname',
            field=models.CharField(blank=True, help_text="Nickname for this address (e.g., 'Mum and Dad', 'The Office', etc)", max_length=50),
        ),
    ]

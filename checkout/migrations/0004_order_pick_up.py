# Generated by Django 3.2.25 on 2024-10-15 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_order_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pick_up',
            field=models.BooleanField(default=False),
        ),
    ]
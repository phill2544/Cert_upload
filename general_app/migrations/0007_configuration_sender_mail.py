# Generated by Django 3.2.16 on 2023-01-28 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_app', '0006_remove_configuration_sender_mail'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='sender_mail',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
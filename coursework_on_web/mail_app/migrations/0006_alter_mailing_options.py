# Generated by Django 4.1.7 on 2023-02-27 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail_app', '0005_mailing_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'permissions': [('set_status', 'Can finish mailing')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]

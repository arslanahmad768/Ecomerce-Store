# Generated by Django 4.2.1 on 2023-05-08 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_order_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['user__first_name', 'user__last_name'], 'permissions': [('view_history', 'Can view history')]},
        ),
    ]

# Generated by Django 3.2.20 on 2023-08-15 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_key_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='key',
            name='link',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]

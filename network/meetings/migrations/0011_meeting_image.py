# Generated by Django 3.2.20 on 2023-10-03 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0010_meeting_np_panel'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='image',
            field=models.ImageField(blank=True, upload_to='meetings/', verbose_name='Картинка'),
        ),
    ]
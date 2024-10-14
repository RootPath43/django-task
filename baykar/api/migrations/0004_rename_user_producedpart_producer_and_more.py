# Generated by Django 4.2.16 on 2024-10-12 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_remove_part_aircraft_remove_part_is_used_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producedpart',
            old_name='user',
            new_name='producer',
        ),
        migrations.AddField(
            model_name='production',
            name='producer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

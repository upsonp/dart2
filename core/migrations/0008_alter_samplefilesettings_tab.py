# Generated by Django 4.2 on 2023-08-15 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_action_sounding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='samplefilesettings',
            name='tab',
            field=models.IntegerField(default=0, help_text='the tab number data is located on', verbose_name='Tab Name'),
        ),
    ]

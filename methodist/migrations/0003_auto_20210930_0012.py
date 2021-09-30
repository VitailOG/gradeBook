# Generated by Django 3.2.7 on 2021-09-29 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('methodist', '0002_auto_20210922_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='educational_program',
        ),
        migrations.AddField(
            model_name='subject',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='methodist.group', verbose_name='Група'),
        ),
    ]

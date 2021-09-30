# Generated by Django 3.2.7 on 2021-09-22 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('methodist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='semester',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Семестер'),
        ),
        migrations.AddField(
            model_name='subject',
            name='final_semester',
            field=models.CharField(blank=True, choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8)], max_length=20, null=True, verbose_name='Кінцевий семестр'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='form_of_control',
            field=models.CharField(choices=[('Залік', 'Залік'), ('Екзамен', 'Екзамен')], max_length=20, verbose_name='Форма конролю'),
        ),
    ]

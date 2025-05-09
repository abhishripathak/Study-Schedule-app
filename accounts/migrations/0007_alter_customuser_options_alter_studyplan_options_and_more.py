# Generated by Django 5.0.6 on 2025-04-21 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_studyplan_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Custom User', 'verbose_name_plural': 'Custom Users'},
        ),
        migrations.AlterModelOptions(
            name='studyplan',
            options={'ordering': ['created_at']},
        ),
        migrations.AddField(
            model_name='studyplan',
            name='available_study_hours',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studyplan',
            name='subjects',
            field=models.TextField(default='No subjects'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='available_study_hours',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studyplan',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='studyplan',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studyplan',
            name='generated_plan',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='studyplan',
            name='preferred_time',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='studyplan',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studyplan',
            name='study_goal',
            field=models.CharField(max_length=255),
        ),
    ]

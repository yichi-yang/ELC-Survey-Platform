# Generated by Django 4.0.1 on 2022-03-05 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0017_remove_surveysubmission_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveysubmission',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='survey.surveysession'),
        ),
    ]

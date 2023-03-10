# Generated by Django 4.1.3 on 2022-12-04 05:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MaxLengthValidator(100)])),
            ],
        ),
        migrations.CreateModel(
            name='GeeksModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Userdata',
            fields=[
                ('email', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('userrole', models.CharField(choices=[('student', 'student'), ('faculty', 'faculty'), ('admin', 'admin')], default='student', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Subcohort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cohort_id', models.ForeignKey(db_constraint=False, default=0, on_delete=django.db.models.deletion.PROTECT, related_name='subcohortid', to='base.cohort')),
                ('parent_id', models.ForeignKey(db_constraint=False, default=0, on_delete=django.db.models.deletion.PROTECT, related_name='subparentid', to='base.cohort')),
            ],
        ),
        migrations.AddField(
            model_name='cohort',
            name='email',
            field=models.ForeignKey(db_constraint=False, default='0', on_delete=django.db.models.deletion.PROTECT, to='base.userdata'),
        ),
    ]

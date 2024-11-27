# Generated by Django 5.1.3 on 2024-11-26 11:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('subject', models.CharField(max_length=50)),
                ('isbn', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'books',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=14, unique=True)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('admission_no', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'db_table': 'students',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('RETURNED', 'Returned'), ('BORROWED', 'Borrowed'), ('LOST', 'Lost')], max_length=50)),
                ('expected_return_date', models.DateField()),
                ('return_date', models.DateField(blank=True, null=True)),
                ('fine', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_app.book')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrower', to='library_app.student')),
            ],
            options={
                'db_table': 'borrowings',
                'ordering': ['book', 'student'],
            },
        ),
    ]

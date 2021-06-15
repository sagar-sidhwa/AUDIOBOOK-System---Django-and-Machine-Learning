# Generated by Django 3.0.1 on 2021-04-23 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audiobookuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=20)),
                ('cpassword', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Pdftemp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ddt', models.DateTimeField()),
                ('ppname', models.CharField(max_length=10)),
                ('ppdf', models.FileField(upload_to='')),
                ('aarange', models.CharField(max_length=10)),
                ('aaname', models.CharField(max_length=10)),
                ('mmp3', models.FileField(upload_to='')),
                ('uu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pdf2mp3.Audiobookuser')),
            ],
        ),
        migrations.CreateModel(
            name='Pdf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateTimeField()),
                ('pname', models.CharField(max_length=10)),
                ('pdf', models.FileField(upload_to='')),
                ('arange', models.CharField(max_length=10)),
                ('aname', models.CharField(max_length=10)),
                ('mp3', models.FileField(upload_to='')),
                ('u', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pdf2mp3.Audiobookuser')),
            ],
        ),
    ]
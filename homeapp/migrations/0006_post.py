# Generated by Django 2.0.5 on 2021-07-22 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0005_delete_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=5000)),
                ('image', models.URLField()),
                ('category', models.CharField(max_length=500)),
                ('summary', models.CharField(max_length=3000)),
                ('content', models.CharField(max_length=50000)),
                ('draft', models.BooleanField(default=False)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='homeapp.Doctor')),
            ],
        ),
    ]

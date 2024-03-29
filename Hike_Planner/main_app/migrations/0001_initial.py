# Generated by Django 4.1.4 on 2023-04-17 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('zipcode', models.IntegerField()),
                ('password', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parkId', models.IntegerField()),
                ('parkRating', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='main_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Park',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('desc', models.TextField()),
                ('long', models.CharField(max_length=255)),
                ('lat', models.CharField(max_length=255)),
                ('img_url', models.CharField(max_length=255)),
                ('img_url2', models.CharField(default='nps.png', max_length=255)),
                ('img_url3', models.CharField(default='nps.png', max_length=255)),
                ('img_url4', models.CharField(default='nps.png', max_length=255)),
                ('img1_desc', models.TextField(null=True)),
                ('img2_desc', models.TextField(null=True)),
                ('img3_desc', models.TextField(null=True)),
                ('img4_desc', models.TextField(null=True)),
                ('parkCode', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('visits', models.ManyToManyField(related_name='visited_parks', to='main_app.user')),
            ],
        ),
    ]

# Generated by Django 3.2.9 on 2021-12-04 04:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время последнего обновления')),
                ('file', models.ImageField(upload_to='photos/', verbose_name='Фотография')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время последнего обновления')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('age', models.PositiveSmallIntegerField(verbose_name='Возраст')),
                ('kind', models.CharField(choices=[('dog', 'Собака'), ('cat', 'Кошка')], max_length=25, verbose_name='Тип')),
                ('photos', models.ManyToManyField(blank=True, related_name='pets', to='pet_api.Photo', verbose_name='Фото')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
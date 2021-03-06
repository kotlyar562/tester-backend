# Generated by Django 2.0.5 on 2018-05-31 22:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('color', models.CharField(default='white', max_length=20, verbose_name='Цвет')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Каталоги',
                'verbose_name': 'Каталог',
            },
        ),
        migrations.CreateModel(
            name='QuestBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Base UUID')),
                ('title', models.CharField(max_length=250, verbose_name='Название базы вопросов')),
                ('klass', models.CharField(blank=True, max_length=100, null=True, verbose_name='Класс')),
                ('discipline', models.CharField(blank=True, max_length=100, null=True, verbose_name='Учебный предмет')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('rating', models.IntegerField(default=0, verbose_name='Рейтинг')),
                ('copi_count', models.IntegerField(default=0, verbose_name='Скопировали раз')),
                ('bought', models.BooleanField(default=False, verbose_name='Купленная')),
                ('copied', models.BooleanField(default=False, verbose_name='Скопированная')),
                ('publik', models.BooleanField(default=False, help_text='Разрешить другим пользователям просматривать и копировать себе базу вопросов', verbose_name='Опубликованная')),
                ('good', models.BooleanField(default=False, verbose_name='Одобрено')),
                ('date_create', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_change', models.DateField(auto_now=True, verbose_name='Дата редактирования')),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bases.Folder', verbose_name='Каталог')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Пользовательские базы вопросов',
                'verbose_name': 'Пользовательская база вопросов',
            },
        ),
    ]

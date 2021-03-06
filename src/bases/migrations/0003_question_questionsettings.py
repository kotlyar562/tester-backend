# Generated by Django 2.0.5 on 2018-06-03 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bases', '0002_auto_20180601_0115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(default='Группа 1', help_text='Разбиение вопросов на группы используется при создании тестов', max_length=100, verbose_name='Группа')),
                ('qtype', models.IntegerField(choices=[(0, 'Один вариант ответа'), (1, 'Несколько вариантов ответа'), (2, 'Ввод ответа'), (3, 'Установить порядок следования')], default=0, verbose_name='Тип вопроса')),
                ('number', models.IntegerField(default=1, verbose_name='Номер вопроса')),
                ('text', models.TextField(verbose_name='Текст вопроса')),
                ('help_text', models.TextField(blank=True, null=True, verbose_name='Комментарий, подсказка')),
                ('base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='bases.QuestBase', verbose_name='База вопросов')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'ordering': ('number',),
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='QuestionSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball', models.IntegerField(default=1, verbose_name='Баллов за правильный ответ на вопрос')),
                ('quest_time', models.PositiveIntegerField(default=0, help_text='В секундах, 0 - неограничено', verbose_name='Время для ответа на этот вопрос')),
                ('random_answers', models.BooleanField(default=True, verbose_name='Варианты ответов в случайном порядке')),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bases.Question', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Настройки вопроса',
                'verbose_name_plural': 'Настройки вопросов',
            },
        ),
    ]

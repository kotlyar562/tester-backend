# Generated by Django 2.0.5 on 2018-06-03 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bases', '0003_question_questionsettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('number', models.IntegerField(default=1, verbose_name='Номер')),
            ],
            options={
                'verbose_name': 'Вариант ответа',
                'verbose_name_plural': 'Варианты ответов',
                'ordering': ('number',),
            },
        ),
        migrations.CreateModel(
            name='AnswerInput',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bases.Answer')),
                ('true_answer', models.CharField(max_length=100, verbose_name='Правильный ответ')),
                ('is_register_dependent', models.BooleanField(default=False, verbose_name='Регистрозависимый текст?')),
                ('is_float_number', models.BooleanField(default=False, help_text='Используйте точку вместо запятой', verbose_name='Вещественное число?')),
            ],
            options={
                'verbose_name': 'Ввод ответа',
                'verbose_name_plural': 'Ввод ответа',
            },
            bases=('bases.answer',),
        ),
        migrations.CreateModel(
            name='AnswerManyAsk',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bases.Answer')),
                ('text', models.TextField(verbose_name='Текст')),
                ('its_true', models.BooleanField(default=False, verbose_name='Правильный ответ')),
            ],
            options={
                'verbose_name': 'Несколько вариантов ответа',
                'verbose_name_plural': 'Несколько вариантов ответа',
            },
            bases=('bases.answer',),
        ),
        migrations.CreateModel(
            name='AnswerOneAsk',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bases.Answer')),
                ('text', models.TextField(verbose_name='Текст')),
                ('its_true', models.BooleanField(default=False, verbose_name='Правильный ответ')),
            ],
            options={
                'verbose_name': 'Один вариант ответа',
                'verbose_name_plural': 'Один вариант ответа',
            },
            bases=('bases.answer',),
        ),
        migrations.CreateModel(
            name='AnswerOrdering',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bases.Answer')),
                ('order_number', models.PositiveIntegerField(default=1, verbose_name='Порядковый номер')),
                ('text', models.TextField(verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Элемент по порядку',
                'verbose_name_plural': 'Элементы по порядку',
            },
            bases=('bases.answer',),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='bases.Question', verbose_name='Вопрос'),
        ),
    ]
# Generated by Django 5.0.1 on 2024-01-21 08:58

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Место проведения квиза')),
                ('address', models.TextField(max_length=100, verbose_name='Адрес места')),
                ('link', models.CharField(max_length=100, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'заведение',
                'verbose_name_plural': 'Заведения',
            },
        ),
        migrations.CreateModel(
            name='QuizGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название квиза')),
                ('level', models.CharField(choices=[('Для новичков', 'Для новичков'), ('Классическая', 'Классическая')], max_length=100, verbose_name='Уровень квиза')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время проведения квиза')),
                ('price', models.IntegerField(verbose_name='Стоимость квиза')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.placequiz')),
            ],
            options={
                'verbose_name': 'игра',
                'verbose_name_plural': 'Игры',
            },
        ),
        migrations.CreateModel(
            name='WriteQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_team', models.CharField(max_length=50, verbose_name='Название команды')),
                ('name_leader', models.CharField(max_length=50, verbose_name='Имя капитана')),
                ('phone_number', models.CharField(max_length=50, verbose_name='Номер телефона')),
                ('email', models.EmailField(max_length=50, verbose_name='Электронная почта')),
                ('count_players', models.IntegerField(verbose_name='Количество участников в команде')),
                ('comment', models.TextField(verbose_name='Комментарий')),
                ('certificate', models.CharField(max_length=50, verbose_name='Сертификат')),
                ('promo_code', models.CharField(max_length=50, verbose_name='Промокод')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время записи на игру')),
                ('quiz_game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.quizgame', verbose_name='Игра')),
            ],
            options={
                'verbose_name': 'запись на игру',
                'verbose_name_plural': 'Записи на игру',
            },
        ),
        migrations.DeleteModel(
            name='Write_quiz',
        ),
    ]
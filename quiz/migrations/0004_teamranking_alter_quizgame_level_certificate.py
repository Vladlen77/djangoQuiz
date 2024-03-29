# Generated by Django 5.0.1 on 2024-01-28 16:32

import django.db.models.deletion
import quiz.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_quizgame_visible'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamRanking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=50, verbose_name='Название команды')),
                ('count_games', models.IntegerField(blank=True, null=True, verbose_name='Количество игр')),
                ('count_scores', models.IntegerField(blank=True, null=True, verbose_name='Количество баллов')),
            ],
            options={
                'verbose_name': 'рейтинг команды',
                'verbose_name_plural': 'Рейтинг команд',
            },
        ),
        migrations.AlterField(
            model_name='quizgame',
            name='level',
            field=models.CharField(choices=[('Классическая', 'Классическая'), ('Для новичков', 'Для новичков')], max_length=100, verbose_name='Уровень квиза'),
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(default=quiz.models.f, max_length=50, unique=True, verbose_name='Сертификат')),
                ('team_ranking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.teamranking')),
            ],
            options={
                'verbose_name': 'сертификат',
                'verbose_name_plural': 'Сертификаты',
            },
        ),
    ]

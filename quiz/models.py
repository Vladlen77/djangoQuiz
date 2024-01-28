import random
import uuid
import string
import secrets
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class PlaceQuiz(models.Model):
    name = models.CharField(max_length=50, verbose_name='Место проведения квиза')
    address = models.TextField(max_length=100, verbose_name='Адрес места')
    link = models.CharField(max_length=100, verbose_name='Ссылка')

    class Meta:
        verbose_name = 'заведение'
        verbose_name_plural = 'Заведения'

    def __str__(self):
        return self.name


class QuizGame(models.Model):
    CHOICES_LEVEL = {
        ('Для новичков', 'Для новичков'),
        ('Классическая', 'Классическая')
    }
    # Название квиза
    name = models.CharField(max_length=100, verbose_name='Название квиза')
    # Уровень квиза
    level = models.CharField(max_length=100, choices=CHOICES_LEVEL, verbose_name='Уровень квиза')
    # Место проведения
    place = models.ForeignKey(PlaceQuiz, on_delete=models.CASCADE)
    # models.CharField(max_length=100, default='Martini', verbose_name='Место проведения квиза'))
    # Дата проведения квиза
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата и время проведения квиза')
    # Цена квиза
    price = models.IntegerField(verbose_name='Стоимость квиза')
    # Запись открыта
    visible = models.BooleanField(default=True, verbose_name='Запись открыта')

    # author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'игра'
        verbose_name_plural = 'Игры'

    def count_team(self, obj):
        result = WriteQuiz.objects.filter(quiz_game=obj).count()
        return result

    def __str__(self):
        return self.name


class WriteQuiz(models.Model):
    # Название команды
    name_team = models.CharField(max_length=50, verbose_name='Название команды')
    # Имя капитана
    name_leader = models.CharField(max_length=50, verbose_name='Имя капитана')
    # Номер телефона
    phone_number = models.CharField(max_length=50, verbose_name='Номер телефона')
    # phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    # Электронная почта
    email = models.EmailField(max_length=50, verbose_name='Электронная почта')
    # Кол-во человек в команде
    count_players = models.IntegerField(verbose_name='Количество участников в команде')
    # Игра
    quiz_game = models.ForeignKey(QuizGame, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Игра')
    # Комментарий к регистрации
    comment = models.TextField(verbose_name='Комментарий')
    # Сертификат
    certificate = models.CharField(max_length=50, verbose_name='Сертификат')
    # Промокод
    promo_code = models.CharField(max_length=50, verbose_name='Промокод')
    # Дата отправки формы
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата и время записи на игру')

    class Meta:
        verbose_name = 'запись на игру'
        verbose_name_plural = 'Записи на игру'

    def __str__(self):
        return self.name_team


def f():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(9))


class TeamRanking(models.Model):
    team = models.CharField(max_length=50, verbose_name='Название команды')
    count_games = models.IntegerField(verbose_name="Количество игр", null=True, blank=True)
    count_scores = models.IntegerField(verbose_name="Количество баллов", null=True, blank=True)

    class Meta:
        verbose_name = 'рейтинг команды'
        verbose_name_plural = 'Рейтинг команд'

    def __str__(self):
        return self.team


class Certificate(models.Model):
    number = models.CharField(max_length=50, verbose_name='Сертификат', default=f, unique=True)
    team_ranking = models.ForeignKey(TeamRanking, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'сертификат'
        verbose_name_plural = 'Сертификаты'

    def __str__(self):
        return self.number

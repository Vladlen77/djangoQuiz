import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


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

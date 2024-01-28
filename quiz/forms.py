from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from .models import WriteQuiz, PlaceQuiz, QuizGame
from django.core.validators import RegexValidator


'''choice_quiz_game = []
quiz_game = QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now())
for i in quiz_game:
    choice_quiz_game.append((i.id, i.place.name + ' - ' + i.place.address))'''


class WriteQuizForm(forms.ModelForm):
    #error_css_class = 'is-invalid'
    name_team_regex = RegexValidator(r'^[0-9a-zA-Zа-яА-я,.?!`()\s-]*$')
    name_team = forms.CharField(validators=[name_team_regex], required=True, max_length=50, widget=forms.TextInput(
        attrs={'id': 'name_team', 'class': 'form-control-custom text-center', 'placeholder': 'Название команды'}),
        error_messages={'invalid': 'Укажите корректное название команды! Допускается использовать русский и английский алфавиты, цифры и следующие знаки: « , », « . », « ? », « ! », « ` », « ( », « ) », « - »'})
    name_leader_regex = RegexValidator(r'^[0-9a-zA-Zа-яА-я,.?!`()\s-]*$')
    name_leader = forms.CharField(validators=[name_leader_regex], required=True, max_length=50, widget=forms.TextInput(
        attrs={'id': 'name_leader', 'class': 'form-control-custom text-center', 'placeholder': 'Имя капитана'}),
        error_messages={'invalid': 'Укажите корректное имя капитана! Допускается использовать русский и английский алфавиты, цифры и следующие знаки: « , », « . », « ? », « ! », « ` », « ( », « ) », « - »'})
    phone_regex = RegexValidator(regex=r'^\+?1?\d{11,11}$')
    phone_number = forms.CharField(validators=[phone_regex], required=True, widget=forms.TextInput(
        attrs={'id': 'phone_number', 'class': 'form-control-custom text-center', 'placeholder': 'Телефон', 'data-mask': 'phone'}),
        error_messages={'invalid': 'Номер телефона необходимо ввести в формате: "+79999999999".'})
    email = forms.EmailField(required=True, max_length=50, widget=forms.EmailInput(
        attrs={'id': 'email', 'class': 'form-control-custom text-center', 'placeholder': 'email'}),
        error_messages={'invalid': 'Укажите корректный email'})
    count_players = forms.IntegerField(label='Количество участников', required=True, min_value=1, max_value=10, widget=forms.NumberInput(
        attrs={'id': 'count_players', 'class': 'form-range', 'type': 'range', 'placeholder': 'Количество участников', 'oninput': "displayrange(this.value)"}))
    #quiz_game = forms.ModelChoiceField(required=True, queryset=QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now()), widget=forms.CheckboxInput(attrs={'id': 'count_players', 'class': 'form-check-input', 'type': 'radio'}))
    #choice_quiz_game = [(i.id, i.name + ' (' + i.place.name + ' - ' + i.place.address + ')') for i in QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now())]
    #quiz_game_ = forms.ChoiceField(required=False, choices=choice_quiz_game, widget=forms.Select(attrs={'id': 'quiz_game', 'class': 'form-select', 'type': 'radio'}))
    #quiz_game_ = forms.ModelChoiceField(queryset=QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now()), required=False, empty_label='None', widget=forms.RadioSelect(
    #    attrs={'id': 'quiz_game', 'class': 'form-check-input'}))
    quiz_game_ = forms.ModelChoiceField(queryset=QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now()), required=False, empty_label='None', widget=forms.RadioSelect(
        attrs={'id': 'quiz_game', 'class': 'form-check'}))
    comment_regex = RegexValidator(r'^[0-9a-zA-Zа-яА-я,.?!`()\s\t\n-]*$')
    comment = forms.CharField(validators=[comment_regex], required=False, widget=forms.Textarea(
        attrs={'id': 'comment', 'class': 'form-control-custom text-center', 'rows': '3', 'placeholder': 'Комментарий'}),
        error_messages={'invalid': 'Укажите комментарий корректно! Допускается использовать русский и английский алфавиты, цифры и следующие знаки: « , », « . », « ? », « ! », « ` », « ( », « ) », « - »'})
    certificate_regex = RegexValidator(r'^[0-9a-zA-Z]*$')
    certificate = forms.CharField(validators=[certificate_regex], required=False, widget=forms.TextInput(
        attrs={'id': 'certificate', 'class': 'form-control-custom text-center', 'rows': '3', 'placeholder': 'Сертификат'}),
        error_messages={'invalid': 'Укажите номер сертификат корректно! Допускается использовать английский алфавиты и цифры.'})

    class Meta:
        model = WriteQuiz
        fields = ('name_team', 'name_leader', 'count_players', 'phone_number', 'email', 'comment', 'certificate')

    def __init__(self, *args, **kwargs):
        quiz_game_ = kwargs.pop('quiz_game_', [])
        super(WriteQuizForm, self).__init__(*args, **kwargs)
        self.fields['quiz_game_'].choices = quiz_game_

    # count_team = WriteQuiz.objects.filter(quiz_game=write_quiz.quiz_game).count()
    '''def count_team(self):
        count_team = WriteQuiz.objects.filter(quiz_game=QuizGame.objects.get(id=self.cleaned_data['quiz_game_'])).count()
        if count_team == 1:
            raise ValidationError("Свободных мест на игру нет")'''

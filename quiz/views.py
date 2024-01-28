import json
from time import strptime
from django import forms
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import QuizGame, WriteQuiz, PlaceQuiz, Certificate, TeamRanking
from .forms import WriteQuizForm
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.core.mail import send_mail
import locale
locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))
import time

import requests
from concurrent.futures import ThreadPoolExecutor

TOKEN = "6786556219:AAG44ZzUG8XOTXeqr4X9_NvLX4k4GktVlqA"
# url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
# print(requests.get(url).json())
chat_id_vlad = "262031692"
chat_id_nikita = "763254172"
chat_id_dasha = "1486946036"
chat_id_kolya = "795626015"


def get_url(url):
    return requests.get(url).json()


def home(request):
    form = WriteQuizForm()
    choice_quiz_game = [(i.id, i.name + ', ' + i.date.strftime('%A, %d %b') + ' (' + i.place.name + ' - ' + i.place.address + ')') for i in
                        QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now()).filter(visible=True)]
    choice_quiz_game_first = QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now()).filter(visible=True).first()
    #print(choice_quiz_game)
    #form.fields["quiz_game_"].choices = choice_quiz_game
    # form.quiz_game_.choices = [(i.id, i.place.name + ' - ' + i.place.address) for i in QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now())]

    if request.method == "POST":
        form = WriteQuizForm(request.POST)
        if form.is_valid():
            #validations
            write_quiz = form.save(commit=False)
            write_quiz.date = timezone.now() + timedelta(hours=3)
            if request.POST.get("quiz_game"):
                q_g = QuizGame.objects.get(id=request.POST.get("quiz_game"))
                #w_q1 = WriteQuiz.objects.filter(name_team=form.cleaned_data['name_team'], quiz_game=q_g).first()
                for w_q in WriteQuiz.objects.filter(name_team=form.cleaned_data['name_team']).all():
                    if (w_q.quiz_game.name in q_g.name) or (q_g.name in w_q.quiz_game.name):
                        print('invalid-dublicate_name_team')
                        response = {
                            'error_name_team': 'invalid-dublicate_name_team',
                        }
                        return JsonResponse(response, status=200)
                for w_q in WriteQuiz.objects.filter(name_leader=form.cleaned_data['name_leader']).all():
                    if (w_q.quiz_game.name in q_g.name) or (q_g.name in w_q.quiz_game.name):
                        print('invalid-dublicate_name_leader')
                        response = {
                            'error_name_leader': 'invalid-dublicate_name_leader',
                        }
                        return JsonResponse(response, status=200)
                write_quiz.quiz_game = q_g
                TeamRanking.objects.get_or_create(team=form.cleaned_data['name_team'])
                team = TeamRanking.objects.filter(team=form.cleaned_data['name_team']).first()
                certifi = Certificate.objects.filter(number=form.cleaned_data['certificate'],
                                                     team_ranking=team).first()
                if form.cleaned_data['certificate'] != '' and not certifi:
                    print('invalid-certificate')
                    response = {
                        'error_certificate': 'invalid-certificate',
                    }
                    return JsonResponse(response, status=200)
            else:
                for i in QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now()):
                    # print(request.POST.get("quiz_game_" + str(i.id)))
                    if request.POST.get("quiz_game_" + str(i.id)):
                        q_g_ = QuizGame.objects.get(id=request.POST.get("quiz_game_" + str(i.id)))
                        for w_q_ in WriteQuiz.objects.filter(name_team=form.cleaned_data['name_team']).all():
                            if (w_q_.quiz_game.name in q_g_.name) or (q_g_.name in w_q_.quiz_game.name):
                                print('invalid-dublicate_name_team')
                                response = {
                                    'error_name_team': 'invalid-dublicate_name_team',
                                }
                                return JsonResponse(response, status=200)
                        for w_q_ in WriteQuiz.objects.filter(name_leader=form.cleaned_data['name_leader']).all():
                            if (w_q_.quiz_game.name in q_g_.name) or (q_g_.name in w_q_.quiz_game.name):
                                print('invalid-dublicate_name_leader')
                                response = {
                                    'error_name_leader': 'invalid-dublicate_name_leader',
                                }
                                return JsonResponse(response, status=200)
                        write_quiz.quiz_game = q_g_
                        TeamRanking.objects.get_or_create(team=form.cleaned_data['name_team'])
                        team = TeamRanking.objects.filter(team=form.cleaned_data['name_team']).first()
                        certifi = Certificate.objects.filter(number=form.cleaned_data['certificate'],
                                                             team_ranking=team).first()
                        if form.cleaned_data['certificate'] != '' and not certifi:
                            print('invalid-certificate')
                            response = {
                                'error_certificate': 'invalid-certificate',
                            }
                            return JsonResponse(response, status=200)
            '''if form.cleaned_data['quiz_game_'] is not None:
                write_quiz.quiz_game = form.cleaned_data['quiz_game_']'''
            write_quiz.count_players = request.POST.get("count_players")
            write_quiz.save()

            response = {
                '': ''
            }

            messages.success(request,
                             'Уважаемый ' + write_quiz.name_leader + '! Ваша команда "' + write_quiz.name_team + '" успешно записана на игру "' + write_quiz.quiz_game.name + '" в ' + write_quiz.quiz_game.place.name + ' (' + write_quiz.quiz_game.date.strftime(
                                 '%A, %d %b') + ')')

            message = ('*' + write_quiz.quiz_game.name + '\n' + write_quiz.quiz_game.place.name + '* (' + write_quiz.quiz_game.date.strftime('%A, %d %b') + ')\n\n' +
                        '- *команда:* ' + write_quiz.name_team +
                        '\n- *капитан*: ' + write_quiz.name_leader + '\n- *телефон*: ' + str(
                    write_quiz.phone_number) + '\n- *email*: ' + write_quiz.email + '\n- *кол-во*: ' + str(
                    write_quiz.count_players) + '\n- *комментарий*: ' + write_quiz.comment)

            message1 = message.replace('.', '\\.')
            message2 = message1.replace('(', '\\(')
            message3 = message2.replace(')', '\\)')
            message4 = message3.replace('-', '\\-')
            message5 = message4.replace('!', '\\!')
            message6 = message5.replace('?', '\\?')
            message7 = message6.replace(',', '\\,')
            message8 = message7.replace('`', '\\`')

            url_vlad = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id_vlad}&text={message8}&parse_mode=MarkdownV2"
            url_nikita = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id_nikita}&text={message8}&parse_mode=MarkdownV2"
            url_dasha = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id_dasha}&text={message8}&parse_mode=MarkdownV2"
            url_kolya = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id_kolya}&text={message8}&parse_mode=MarkdownV2"
            urls = [url_vlad, url_nikita, url_dasha, url_kolya]

            '''with ThreadPoolExecutor(max_workers=3) as pool:
                list(pool.map(get_url, urls))'''
            time.sleep(3)
            # print(list(pool.map(get_url, urls)))
            # requests.get(url_vlad).json()
            # requests.get(url_nikita).json()
            # requests.get(url_dasha).json()
            # requests.get(url_kolya).json()
            '''send_mail(
                "Запись на квиз Break Brain",
                ["Команда " + write_quiz.name_team + ' успешно записана на игру ' + write_quiz.quiz_game.name + ' в ' + write_quiz.quiz_game.place.name],
                "breakbrainquiz@mail.ru",
                [write_quiz.email],
                fail_silently=False,
            )'''
            print('red')
            # return redirect('quiz-timetable')
            return JsonResponse(response, status=200)
        else:
            print('eer')
            if request.POST.get("quiz_game"):
                q_g = QuizGame.objects.get(id=request.POST.get("quiz_game"))
                # w_q1 = WriteQuiz.objects.filter(name_team=form.cleaned_data['name_team'], quiz_game=q_g).first()
                for w_q in WriteQuiz.objects.filter(name_team=request.POST.get("name_team")).all():
                    if (w_q.quiz_game.name in q_g.name) or (q_g.name in w_q.quiz_game.name):
                        print('invalid-dublicate_name_team')
                        response = {
                            'errors': form.errors,
                            'error_name_team': 'invalid-dublicate_name_team',
                        }
                        return JsonResponse(response, status=200)
                for w_q in WriteQuiz.objects.filter(name_leader=request.POST.get("name_leader")).all():
                    if (w_q.quiz_game.name in q_g.name) or (q_g.name in w_q.quiz_game.name):
                        print('invalid-dublicate_name_leader')
                        response = {
                            'errors': form.errors,
                            'error_name_leader': 'invalid-dublicate_name_leader',
                        }
                        return JsonResponse(response, status=200)
            else:
                for i in QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now()):
                    # print(request.POST.get("quiz_game_" + str(i.id)))
                    if request.POST.get("quiz_game_" + str(i.id)):
                        q_g_ = QuizGame.objects.get(id=request.POST.get("quiz_game_" + str(i.id)))
                        for w_q_ in WriteQuiz.objects.filter(name_team=request.POST.get("name_team")).all():
                            if (w_q_.quiz_game.name in q_g_.name) or (q_g_.name in w_q_.quiz_game.name):
                                print('invalid-dublicate_name_team')
                                response = {
                                    'errors': form.errors,
                                    'error_name_team': 'invalid-dublicate_name_team',
                                }
                                return JsonResponse(response, status=200)
                        for w_q_ in WriteQuiz.objects.filter(name_leader=request.POST.get("name_leader")).all():
                            if (w_q_.quiz_game.name in q_g_.name) or (q_g_.name in w_q_.quiz_game.name):
                                print('invalid-dublicate_name_leader')
                                response = {
                                    'errors': form.errors,
                                    'error_name_leader': 'invalid-dublicate_name_leader',
                                }
                                return JsonResponse(response, status=200)
            response = {
                'errors': form.errors,
            }
            return JsonResponse(response, status=200)
    data = {
        'quiz_game': QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now()),
        'title': 'Главная страница',
        'form': form,
        'choice_quiz_game': choice_quiz_game,
        'choice_quiz_game_first': choice_quiz_game_first
    }
    return render(request, 'quiz/home.html', data)


def timetable(request):
    form = WriteQuizForm()
    choice_quiz_game = [(i.id, i.name + ' (' + i.place.name + ' - ' + i.place.address + ')') for i in
                        QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now()).filter(visible=True)]
    choice_quiz_game_first = QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now()).filter(visible=True).first()
    #form.fields["quiz_game_"].choices = choice_quiz_game
    # form.quiz_game_.choices = [(i.id, i.place.name + ' - ' + i.place.address) for i in QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now())]

    if request.method == "POST":
        #print('-----ВОШЛИ 4444------')
        #print(request.POST)
        form = WriteQuizForm(request.POST)
        #print(form.is_valid())
        # print(form)
        if form.is_valid():
            write_quiz = form.save(commit=False)
            write_quiz.date = timezone.now() + timedelta(hours=3)
            if request.POST.get("quiz_game"):
                q_g = QuizGame.objects.get(id=request.POST.get("quiz_game"))
                # w_q1 = WriteQuiz.objects.filter(name_team=form.cleaned_data['name_team'], quiz_game=q_g).first()
                for w_q in WriteQuiz.objects.filter(name_team=form.cleaned_data['name_team']).all():
                    if (w_q.quiz_game.name in q_g.name) or (q_g.name in w_q.quiz_game.name):
                        print('invalid-dublicate_name_team')
                        response = {
                            'error_name_team': 'invalid-dublicate_name_team',
                        }
                        return JsonResponse(response, status=200)
                for w_q in WriteQuiz.objects.filter(name_leader=form.cleaned_data['name_leader']).all():
                    if (w_q.quiz_game.name in q_g.name) or (q_g.name in w_q.quiz_game.name):
                        print('invalid-dublicate_name_leader')
                        response = {
                            'error_name_leader': 'invalid-dublicate_name_leader',
                        }
                        return JsonResponse(response, status=200)
                write_quiz.quiz_game = q_g
                TeamRanking.objects.get_or_create(team=form.cleaned_data['name_team'])
                team = TeamRanking.objects.filter(team=form.cleaned_data['name_team']).first()
                certifi = Certificate.objects.filter(number=form.cleaned_data['certificate'],
                                                     team_ranking=team).first()
                if form.cleaned_data['certificate'] != '' and not certifi:
                    print('invalid-certificate')
                    response = {
                        'error_certificate': 'invalid-certificate',
                    }
                    return JsonResponse(response, status=200)
            else:
                for i in QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now()):
                    # print(request.POST.get("quiz_game_" + str(i.id)))
                    if request.POST.get("quiz_game_" + str(i.id)):
                        q_g_ = QuizGame.objects.get(id=request.POST.get("quiz_game_" + str(i.id)))
                        for w_q_ in WriteQuiz.objects.filter(name_team=form.cleaned_data['name_team']).all():
                            if (w_q_.quiz_game.name in q_g_.name) or (q_g_.name in w_q_.quiz_game.name):
                                print('invalid-dublicate_name_team')
                                response = {
                                    'error_name_team': 'invalid-dublicate_name_team',
                                }
                                return JsonResponse(response, status=200)
                        for w_q_ in WriteQuiz.objects.filter(name_leader=form.cleaned_data['name_leader']).all():
                            if (w_q_.quiz_game.name in q_g_.name) or (q_g_.name in w_q_.quiz_game.name):
                                print('invalid-dublicate_name_leader')
                                response = {
                                    'error_name_leader': 'invalid-dublicate_name_leader',
                                }
                                return JsonResponse(response, status=200)
                        write_quiz.quiz_game = q_g_
                        TeamRanking.objects.get_or_create(team=form.cleaned_data['name_team'])
                        team = TeamRanking.objects.filter(team=form.cleaned_data['name_team']).first()
                        certifi = Certificate.objects.filter(number=form.cleaned_data['certificate'],
                                                             team_ranking=team).first()
                        if form.cleaned_data['certificate'] != '' and not certifi:
                            print('invalid-certificate')
                            response = {
                                'error_certificate': 'invalid-certificate',
                            }
                            return JsonResponse(response, status=200)
            '''if form.cleaned_data['quiz_game_'] is not None:
                write_quiz.quiz_game = form.cleaned_data['quiz_game_']'''
            write_quiz.count_players = request.POST.get("count_players")
            write_quiz.save()
            response = {
                '': ''
            }
            '''output = {
                'name_team': write_quiz.name_team,
                'name_leader': write_quiz.name_leader,
                'phone_number': write_quiz.phone_number,
                'email': write_quiz.email,
                'count_players': write_quiz.count_players,
                'comment': write_quiz.comment
            }'''
            messages.success(request,
                             'Уважаемый ' + write_quiz.name_leader + '! Ваша команда "' + write_quiz.name_team + '" успешно записана на игру "' + write_quiz.quiz_game.name + '" в ' + write_quiz.quiz_game.place.name + ' (' + write_quiz.quiz_game.date.strftime('%A, %d %b') + ')')
            message = ('*' + write_quiz.quiz_game.name + '\n' + write_quiz.quiz_game.place.name + '* (' + write_quiz.quiz_game.date.strftime('%A, %d %b') + ')\n\n' +
                       '- *команда:* ' + write_quiz.name_team +
                       '\n- *капитан*: ' + write_quiz.name_leader + '\n- *телефон*: ' + str(
                        write_quiz.phone_number) + '\n- *email*: ' + write_quiz.email + '\n- *кол-во*: ' + str(
                        write_quiz.count_players) + '\n- *комментарий*: ' + write_quiz.comment)
            message1 = message.replace('.', '\\.')
            message2 = message1.replace('(', '\\(')
            message3 = message2.replace(')', '\\)')
            message4 = message3.replace('-', '\\-')
            message5 = message4.replace('!', '\\!')
            message6 = message5.replace('?', '\\?')
            message7 = message6.replace(',', '\\,')
            message8 = message7.replace('`', '\\`')

            url_vlad = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id_vlad}&text={message8}&parse_mode=MarkdownV2"
            url_nikita = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id_nikita}&text={message8}&parse_mode=MarkdownV2"
            url_dasha = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id_dasha}&text={message8}&parse_mode=MarkdownV2"
            url_kolya = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id_kolya}&text={message8}&parse_mode=MarkdownV2"
            urls = [url_vlad, url_nikita, url_dasha, url_kolya]

            '''with ThreadPoolExecutor(max_workers=3) as pool:
                list(pool.map(get_url, urls))'''
            time.sleep(3)
                #print(list(pool.map(get_url, urls)))
            #requests.get(url_vlad).json()
            #requests.get(url_nikita).json()
            #requests.get(url_dasha).json()
            #requests.get(url_kolya).json()
            '''send_mail(
                "Запись на квиз Break Brain",
                ["Команда " + write_quiz.name_team + ' успешно записана на игру ' + write_quiz.quiz_game.name + ' в ' + write_quiz.quiz_game.place.name],
                "breakbrainquiz@mail.ru",
                [write_quiz.email],
                fail_silently=False,
            )'''
            # return JsonResponse({"name": write_quiz.name_leader}, status=200)
            print('red')
            # return redirect('quiz-timetable')
            return JsonResponse(response, status=200)
        else:
            print('eer')
            if request.POST.get("quiz_game"):
                q_g = QuizGame.objects.get(id=request.POST.get("quiz_game"))
                # w_q1 = WriteQuiz.objects.filter(name_team=form.cleaned_data['name_team'], quiz_game=q_g).first()
                for w_q in WriteQuiz.objects.filter(name_team=request.POST.get("name_team")).all():
                    if (w_q.quiz_game.name in q_g.name) or (q_g.name in w_q.quiz_game.name):
                        print('invalid-dublicate_name_team')
                        response = {
                            'errors': form.errors,
                            'error_name_team': 'invalid-dublicate_name_team',
                        }
                        return JsonResponse(response, status=200)
                for w_q in WriteQuiz.objects.filter(name_leader=request.POST.get("name_leader")).all():
                    if (w_q.quiz_game.name in q_g.name) or (q_g.name in w_q.quiz_game.name):
                        print('invalid-dublicate_name_leader')
                        response = {
                            'errors': form.errors,
                            'error_name_leader': 'invalid-dublicate_name_leader',
                        }
                        return JsonResponse(response, status=200)
            else:
                for i in QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now()):
                    # print(request.POST.get("quiz_game_" + str(i.id)))
                    if request.POST.get("quiz_game_" + str(i.id)):
                        q_g_ = QuizGame.objects.get(id=request.POST.get("quiz_game_" + str(i.id)))
                        for w_q_ in WriteQuiz.objects.filter(name_team=request.POST.get("name_team")).all():
                            if (w_q_.quiz_game.name in q_g_.name) or (q_g_.name in w_q_.quiz_game.name):
                                print('invalid-dublicate_name_team')
                                response = {
                                    'errors': form.errors,
                                    'error_name_team': 'invalid-dublicate_name_team',
                                }
                                return JsonResponse(response, status=200)
                        for w_q_ in WriteQuiz.objects.filter(name_leader=request.POST.get("name_leader")).all():
                            if (w_q_.quiz_game.name in q_g_.name) or (q_g_.name in w_q_.quiz_game.name):
                                print('invalid-dublicate_name_leader')
                                response = {
                                    'errors': form.errors,
                                    'error_name_leader': 'invalid-dublicate_name_leader',
                                }
                                return JsonResponse(response, status=200)
            response = {
                'errors': form.errors,
            }
            return JsonResponse(response, status=200)
    data = {
        'quiz_game': QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now()),
        'title': 'Расписание интеллектуальных игр Break Brain',
        'form': form,
        'choice_quiz_game': choice_quiz_game,
        'choice_quiz_game_first': choice_quiz_game_first
    }
    return render(request, 'quiz/timetable.html', data)


def rules(request):
    form = WriteQuizForm()
    choice_quiz_game = [(i.id, i.name + ' (' + i.place.name + ' - ' + i.place.address + ')') for i in
                        QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now()).filter(visible=True)]
    choice_quiz_game_first = QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now()).filter(visible=True).first()
    #form.fields["quiz_game_"].choices = choice_quiz_game
    #form.fields['quiz_game_'].empty_label = choice_quiz_game[2]
    #print(choice_quiz_game)
    #print(choice_quiz_game[0])
    if request.method == "POST":
        form = WriteQuizForm(request.POST)
        if form.is_valid():
            write_quiz = form.save(commit=False)
            write_quiz.date = timezone.now() + timedelta(hours=3)
            if request.POST.get("quiz_game"):
                q_g = QuizGame.objects.get(id=request.POST.get("quiz_game"))
                # w_q1 = WriteQuiz.objects.filter(name_team=form.cleaned_data['name_team'], quiz_game=q_g).first()
                for w_q in WriteQuiz.objects.filter(name_team=form.cleaned_data['name_team']).all():
                    if (w_q.quiz_game.name in q_g.name) or (q_g.name in w_q.quiz_game.name):
                        print('invalid-dublicate_name_team')
                        response = {
                            'error_name_team': 'invalid-dublicate_name_team',
                        }
                        return JsonResponse(response, status=200)
                for w_q in WriteQuiz.objects.filter(name_leader=form.cleaned_data['name_leader']).all():
                    if (w_q.quiz_game.name in q_g.name) or (q_g.name in w_q.quiz_game.name):
                        print('invalid-dublicate_name_leader')
                        response = {
                            'error_name_leader': 'invalid-dublicate_name_leader',
                        }
                        return JsonResponse(response, status=200)
                write_quiz.quiz_game = q_g
                TeamRanking.objects.get_or_create(team=form.cleaned_data['name_team'])
                team = TeamRanking.objects.filter(team=form.cleaned_data['name_team']).first()
                certifi = Certificate.objects.filter(number=form.cleaned_data['certificate'],
                                                     team_ranking=team).first()
                if form.cleaned_data['certificate'] != '' and not certifi:
                    print('invalid-certificate')
                    response = {
                        'error_certificate': 'invalid-certificate',
                    }
                    return JsonResponse(response, status=200)
            '''if form.cleaned_data['quiz_game_'] is not None:
                write_quiz.quiz_game = form.cleaned_data['quiz_game_']'''
            write_quiz.count_players = request.POST.get("count_players")
            write_quiz.save()
            response = {
                '': ''
            }

            messages.success(request,
                             'Уважаемый ' + write_quiz.name_leader + '! Ваша команда "' + write_quiz.name_team + '" успешно записана на игру "' + write_quiz.quiz_game.name + '" в ' + write_quiz.quiz_game.place.name + ' (' + write_quiz.quiz_game.date.strftime(
                                 '%A, %d %b') + ')')
            message = ('*' + write_quiz.quiz_game.name + '\n' + write_quiz.quiz_game.place.name + '* (' + write_quiz.quiz_game.date.strftime('%A, %d %b') + ')\n\n' +
                        '- *команда:* ' + write_quiz.name_team +
                        '\n- *капитан*: ' + write_quiz.name_leader + '\n- *телефон*: ' + str(
                    write_quiz.phone_number) + '\n- *email*: ' + write_quiz.email + '\n- *кол-во*: ' + str(
                    write_quiz.count_players) + '\n- *комментарий*: ' + write_quiz.comment)
            message1 = message.replace('.', '\\.')
            message2 = message1.replace('(', '\\(')
            message3 = message2.replace(')', '\\)')
            message4 = message3.replace('-', '\\-')
            message5 = message4.replace('!', '\\!')
            message6 = message5.replace('?', '\\?')
            message7 = message6.replace(',', '\\,')
            message8 = message7.replace('`', '\\`')

            url_vlad = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id_vlad}&text={message8}&parse_mode=MarkdownV2"
            url_nikita = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id_nikita}&text={message8}&parse_mode=MarkdownV2"
            url_dasha = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id_dasha}&text={message8}&parse_mode=MarkdownV2"
            url_kolya = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id_kolya}&text={message8}&parse_mode=MarkdownV2"
            urls = [url_vlad, url_nikita, url_dasha, url_kolya]

            '''with ThreadPoolExecutor(max_workers=3) as pool:
                list(pool.map(get_url, urls))'''
            time.sleep(3)

            '''send_mail(
                "Запись на квиз Break Brain",
                ["Команда " + write_quiz.name_team + ' успешно записана на игру ' + write_quiz.quiz_game.name + ' в ' + write_quiz.quiz_game.place.name],
                "breakbrainquiz@mail.ru",
                [write_quiz.email],
                fail_silently=False,
            )'''
            return JsonResponse(status=200, data=response)
        else:
            print('eer')
            if request.POST.get("quiz_game"):
                q_g = QuizGame.objects.get(id=request.POST.get("quiz_game"))
                # w_q1 = WriteQuiz.objects.filter(name_team=form.cleaned_data['name_team'], quiz_game=q_g).first()
                for w_q in WriteQuiz.objects.filter(name_team=request.POST.get("name_team")).all():
                    if (w_q.quiz_game.name in q_g.name) or (q_g.name in w_q.quiz_game.name):
                        print('invalid-dublicate_name_team')
                        response = {
                            'errors': form.errors,
                            'error_name_team': 'invalid-dublicate_name_team',
                        }
                        return JsonResponse(response, status=200)
                for w_q in WriteQuiz.objects.filter(name_leader=request.POST.get("name_leader")).all():
                    if (w_q.quiz_game.name in q_g.name) or (q_g.name in w_q.quiz_game.name):
                        print('invalid-dublicate_name_leader')
                        response = {
                            'errors': form.errors,
                            'error_name_leader': 'invalid-dublicate_name_leader',
                        }
                        return JsonResponse(response, status=200)
            response = {
                'errors': form.errors,
            }
            return JsonResponse(response, status=200)
    data = {
        'quiz_game': QuizGame.objects.all().order_by('date').filter(date__gte=timezone.now()),
        'title': 'Правила интеллектуальной игры Break Brain',
        'form': form,
        'choice_quiz_game': choice_quiz_game,
        'choice_quiz_game_first': choice_quiz_game_first
    }
    return render(request, 'quiz/rules.html', data)

from django.contrib import admin

# Register your models here.
from .models import WriteQuiz, QuizGame, PlaceQuiz, Certificate, TeamRanking


class WriteQuizInline(admin.StackedInline):
    model = WriteQuiz
    extra = 0


# admin.site.register(WriteQuiz)
@admin.register(WriteQuiz)
class WriteQuizAdmin(admin.ModelAdmin):
    list_display = ('name_team', 'name_leader', 'phone_number', 'email', 'quiz_game', 'date')
    list_filter = ('quiz_game', 'date')
    search_fields = ('name_team', 'name_leader', 'phone_number', 'email')


# admin.site.register(QuizGame)
@admin.register(QuizGame)
class QuizGameAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'place', 'date', 'visible', 'count_team')
    list_filter = ('name', 'level', 'place', 'date')
    search_fields = ('name', 'level', 'date')

    def count_team(self, obj):
        result = WriteQuiz.objects.filter(quiz_game=obj).count()
        return result


# admin.site.register(PlaceQuiz)
@admin.register(PlaceQuiz)
class PlaceQuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'link')
    list_filter = ('name', 'address', 'link')
    search_fields = ('name', 'address', 'link')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('number', 'team_ranking')
    list_filter = ('number', 'team_ranking')
    search_fields = ('number', )


@admin.register(TeamRanking)
class TeamRankingAdmin(admin.ModelAdmin):
    list_display = ('team', 'count_games', 'count_scores')
    list_filter = ('team',)
    search_fields = ('team',)

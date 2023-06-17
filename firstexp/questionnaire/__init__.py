from otree.api import *


doc = """
A simple questionnaire
"""


class C(BaseConstants):
    NAME_IN_URL = 'questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    school = models.StringField(
        label = '您就读的学校是',
    )
    age = models.IntegerField(
        min = 0,
        max = 99,
        label = '您的年龄是',
    )
    #dropdown menu
    gender = models.IntegerField(
        choices = [
            [0,'女'],
            [1,'男'],
        ],
        label = '您的性别是',
    )
    #horizontal radio buttons
    grade = models.IntegerField(
        choices = [
            [1,'大一'],
            [2,'大二'],
            [3,'大三'],
            [4,'大四'],
            [5,'硕士生'],
            [6,'博士生'],
        ],
        widget = widgets.RadioSelectHorizontal,
        label = '您的年级'
    )
    #vertical radio buttons
    major = models.BooleanField(
        choice = [
            [False,'否'],
            [True,'是'],
        ],
        widget = widgets.RadioSelect,
        label = '您是否主修经济类专业？',
    )
    suggest = models.LongStringField(
        blank = True,
        label = '如果您有意见或建议，请填写在下框中',
    )
    attention = models.IntegerField(
        label = '请在下框内填入1234以提交本页'
    )


# PAGES
class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['school','age','gender','grade','major','suggest','attention']

    @staticmethod
    def error_message(player,values):
        if values['attention'] != 1234:
            return '输入有误！'


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    
    @staticmethod
    def vars_for_template(player):
        if player.gender == 0:
            gender_text = '女'
        else:
            gender_text = '男'
        if player.grade <= 4:
            grade_text = '本科生'
        else:
            grade_text = '研究生'
        return dict(
            gender_text = gender_text,
            grade_text = grade_text
        )


page_sequence = [Questionnaire, Results]

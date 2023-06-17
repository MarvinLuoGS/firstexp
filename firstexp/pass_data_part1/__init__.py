from otree.api import *


doc = """
Example for passing data-part1
"""


class C(BaseConstants):
    NAME_IN_URL = 'pass_data_part1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass_number = models.IntegerField(label='输入一个数字用于在round和app之间传递')



# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['pass_number']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant #获取player的participant
        participant.pass_number = player.pass_number #将player的pass_number传给participant
        #participant.var这样的写法就是使用participant类中的字段
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    
    @staticmethod
    def vars_for_template(player: Player):
        prev_player = player.in_round(1) #获取第1轮的player对象
        number_round_1 = prev_player.pass_number
        return dict(
            number_round_1 = number_round_1 #为页面展示准备的变量
            #前端不允许player.in_round(1).pass_number这样的写法，所以需要转换以下
        )
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2


page_sequence = [MyPage, Results]

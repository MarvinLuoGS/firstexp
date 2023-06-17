from otree.api import *


doc = """
Example for currency
"""


class C(BaseConstants):
    NAME_IN_URL = 'currency'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    earned = models.CurrencyField(label='往earned字段中输入一个数字')

#定义收益计算函数
def set_payoff(player):
    player.payoff = 2 * player.earned


# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['earned']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        set_payoff(player) #调用收益计算函数


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        participant = player.participant
        return dict(
            participation_fee = session.config['participation_fee'], #用于前端展示出场费
            payoff_cu = participant.payoff.to_real_world_currency(session), #用于前端展示实际货币计算的任务收益
            total_payment = participant.payoff_plus_participation_fee() #用于前端展示总收益
        )


page_sequence = [MyPage,Results]

from otree.api import *




doc = """
Example for trust game
"""


class C(BaseConstants):
    NAME_IN_URL = 'trust_game'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 5
    
    ENDOWMENT = cu(100)
    MULTIPLIER = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        min=cu(0),
        max=C.ENDOWMENT,
        label="请输入您要发送的点数",
    )
    sent_back_amount = models.CurrencyField(
        min=cu(0),
        label="请输入您要返还的点数："
        )


class Player(BasePlayer):
    pass


# FUNCTIONS
def sent_back_amount_max(group: Group):
    return group.sent_amount * C.MULTIPLIER


def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount
    p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount


def creating_session(subsession):
    subsession.group_randomly(fixed_id_in_group=True)


# PAGES
class Introduction(Page):

    @staticmethod
    def vars_for_template(player: Player):
        if player.id_in_group == 1:
            role_text = '角色A'
        else:
            role_text = '角色B'
        return dict(
            role_text = role_text
        )
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Send(Page):
    form_model = 'group'
    form_fields = ['sent_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class SendBackWaitPage(WaitPage):
    title_text = '请耐心等待！'
    body_text = '请保持安静，如果有问题，请询问实验员。'


class SendBack(Page):
    form_model = 'group'
    form_fields = ['sent_back_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        tripled_amount = group.sent_amount * C.MULTIPLIER
        return dict(tripled_amount=tripled_amount)


class ResultsWaitPage(WaitPage):
    title_text = '请耐心等待！'
    body_text = '请保持安静，如果有问题，请询问实验员。'

    after_all_players_arrive = set_payoffs


class Results(Page):

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(tripled_amount=group.sent_amount * C.MULTIPLIER)


page_sequence = [
    Introduction,
    Send,
    SendBackWaitPage,
    SendBack,
    ResultsWaitPage,
    Results,
]

from otree.api import *


doc = """
Example for public goods game
"""


class C(BaseConstants):
    NAME_IN_URL = 'publicgood'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 5

    ENDOWMENT = cu(200)
    MULTIPLIER = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min = 0,
        max = C.ENDOWMENT,
        label = "请输入您的贡献额"
    )


def creating_session(subsession):
    subsession.group_randomly()


def set_payoffs(group:Group):
    player_list = group.get_players() #获得包含小组内所有玩家的列表
    contribution_list = [p.contribution for p in player_list] #获得小组内所有贡献额列表
    group.total_contribution = sum(contribution_list) #求得贡献额总和
    group.individual_share = group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    for p in player_list: #对小组内的每一个玩家，减去自己的贡献额后加上分得的收益
        p.payoff = C.ENDOWMENT - p.contribution + group.individual_share


# PAGES
class Contribution(Page):
    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    title_text = '请耐心等待！'
    body_text = '请保持安静，如果有问题，请询问实验员。'

    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs(group)
    
    #wait_for_all_groups = True
    #@staticmethod
    #def after_all_players_arrive(subsession: Subsession):
    #    group_list = subsession.get_groups()
    #    for g in group_list:
    #        set_payoffs(g)


class Results(Page):
    pass


page_sequence = [Contribution, ResultsWaitPage, Results]

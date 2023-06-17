from otree.api import *


doc = """
Example for passing data-part2
"""


class C(BaseConstants):
    NAME_IN_URL = 'pass_data_part2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Results]

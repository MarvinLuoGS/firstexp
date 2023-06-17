from otree.api import *


doc = """
Example for timer
"""


class C(BaseConstants):
    NAME_IN_URL = 'timer'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Timer1(Page):
    timeout_seconds = 20
    timer_text = '当前页面的剩余时间'


class Timer2(Page):
    timeout_seconds = 20
    

class Timer3(Page):
    pass


class Timer4(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [
    Timer1,
    Timer2,
    Timer3,
    Timer4
    ]

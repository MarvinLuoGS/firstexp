from os import environ

SESSION_CONFIGS = [
    dict(
        name = 'data_sample',
        display_name = 'data_sample',
        app_sequence = ['trustgame','questionnaire'],
        num_demo_participants = 2,
    ),
     dict(
        name = 'questionnaire',
        display_name = 'questionnaire',
        app_sequence = ['questionnaire'],
        num_demo_participants = 2,
    ),
    dict(
        name = 'publicgood',
        display_name = 'publicgood',
        app_sequence = ['publicgood'],
        num_demo_participants = 6,
    ),
    dict(
        name = 'trustgame',
        display_name = 'trustgame',
        app_sequence = ['trustgame'],
        num_demo_participants = 2,
    ),
    dict(
        name = 'group_matching',
        display_name = 'group_matching',
        app_sequence = ['group_matching'],
        num_demo_participants = 6,
    ),
    dict(
        name = 'pass_data',
        display_name = 'pass_data',
        app_sequence =['pass_data_part1','pass_data_part2'],
        num_demo_participants = 1
    ),
    dict(
        name = 'timer',
        display_name = 'timer',
        app_sequence =['timer'],
        num_demo_participants = 1
    ),
    dict(
        name = 'currency',
        display_name = 'currency',
        app_sequence =['currency'],
        num_demo_participants = 1
    )
]

ROOMS = [
    dict(
        name = 'Econ',
        display_name = 'Econ',
        participant_label_file = '_rooms/Econ.txt',
        #use_secure_urls = True,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.50, participation_fee=10.00, doc=""
)

PARTICIPANT_FIELDS = ['pass_number']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'zh-hans'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'CNY'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5552739159576'

DEBUG = False
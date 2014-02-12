from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# ======================================================================================================== #
#                                      Session/Security Configuration                                      #
# ======================================================================================================== #

# Cookie Settings
SESSION_COOKIE_NAME = 'SchedulesSessionID'


ALLOWED_HOSTS = [
    'schedules.kavanaughdevelopment.com',
]
from .base import *

# ======================================================================================================== #
#                                         Test Settings                                                    #
# ======================================================================================================== #

TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'


# ======================================================================================================== #
#                                          Database Configuration                                          #
# ======================================================================================================== #

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

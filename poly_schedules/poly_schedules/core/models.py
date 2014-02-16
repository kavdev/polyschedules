"""
.. module:: poly_schedules.core.models
   :synopsis: Poly Schedules Core Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import re

from django.contrib.auth.models import AbstractUser
from django.db.models import ManyToManyField, BooleanField, PositiveIntegerField
from django.core.mail import send_mail

from votes.models import Vote
from preferences.models import CoursePreference
from schedules.models import Day


class PolySchedulesUser(AbstractUser):
    """Poly Schedules User Model."""

    # Instructor Fields
    wtu = PositiveIntegerField(default=0)
    time_preferences = ManyToManyField(Day)
    course_preferences = ManyToManyField(CoursePreference)
    preferences_locked = BooleanField(default=False)
    is_active_instructor = BooleanField(default=True)

    # Student Fields
    votes = ManyToManyField(Vote)

    #
    # A set of flags for each user that decides what the user can and cannot see.
    #
    is_instructor = BooleanField(default=False)  # Instructors

    class Meta:
        verbose_name = u'Poly Schedules User'
        verbose_name_plural = u'Poly Schedules Users'

    def get_full_name(self):
        """Returns the first_name plus the last_name with a space in between and the possible '- ADMIN' removed."""

        full_name = '%s %s' % (self.first_name, re.sub(r' - ADMIN', '', self.last_name))
        return full_name.strip()

    def get_alias(self):
        """Returns the username with the possible '-admin' removed."""

        return re.sub(r'-admin', '', self.username)

    def email_user(self, subject, message, from_email=None):
        """Sends an email to this User."""

        send_mail(subject, message, from_email, [self.email])

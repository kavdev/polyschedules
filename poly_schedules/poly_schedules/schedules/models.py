"""
.. module:: poly_schedules.schedules.models
   :synopsis: Poly Schedules Schedule Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import datetime

from django.conf import settings
from django.db.models import Model
from django.db.models.fields import PositiveSmallIntegerField, DecimalField, DateField, TimeField, CharField, IntegerField, BooleanField
from django.db.models.fields.related import ForeignKey, ManyToManyField


from .fields import BooleanListField


class Course(Model):
    PROXIMITIES = ['DIRECTLY_AFTER', 'SAME_DAY', 'DIFFERENT_DAY']

    prefix = CharField(max_length=4)
    number = PositiveSmallIntegerField()
    title = CharField(max_length=60)
    units = PositiveSmallIntegerField(default=4)
    wtu = PositiveSmallIntegerField(default=5)
    requires_equipment = BooleanField(default=False)

    # Lab Fields
    has_lab = BooleanField()
    lab_requires_equiment = BooleanField(default=False)
    lab_length = DecimalField(max_digits=3, decimal_places=2, verbose_name='Lab Length (Hours)')
    lab_time_proximity = PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return self.prefix + " " + str(self.number)

    class Meta:
        unique_together = ("prefix", "number")


class Location(Model):
    building = CharField(max_length=60)
    building_number = CharField(max_length=4)
    room_number = CharField(max_length=4)
    has_equipment = BooleanField(default=False)
    capacity = PositiveSmallIntegerField()
    availability = ForeignKey('Week', unique=True)

    def __unicode__(self):
        return self.building + " (" + self.building_number + ") " + self.room_number

    class Meta:
        unique_together = ("building_number", "room_number")


class Section(Model):
    course = ForeignKey(Course)
    number = PositiveSmallIntegerField()
    instructor = ForeignKey(settings.AUTH_USER_MODEL)
    location = ForeignKey(Location)
    times = ManyToManyField('SectionTime')

    # The associated lab, if it exists
    associated_lab = ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.course + " - " + str(self.number)

    class Meta:
        unique_together = ("course", "number")


class SectionTime(Model):

    TIME_PATTERNS = ['MWF', 'MW', 'MF', 'WF', 'TH', 'MTWH', 'MTWF']
    TIME_PATTERN_CHOICES = [(TIME_PATTERNS.index(time_pattern), time_pattern) for time_pattern in TIME_PATTERNS]

    time_pattern = IntegerField(choices=TIME_PATTERN_CHOICES)
    start_time = TimeField()
    length = DecimalField(max_digits=3, decimal_places=2, verbose_name='Length (Hours)')

    def __unicode__(self):
        length_digits = self.length.as_tuple().digits
        length_hours = length_digits[0]
        length_minutes = (60 * ((length_digits[1] * 10) + length_digits[2])) / 100  # Integer math gets nice minute numbers

        end_time = self.start_time + datetime.timedelta(hours=length_hours, minutes=length_minutes)

        return self.TIME_PATTERNS[self.time_pattern] + " " + str(self.start_time) + " - " + str(end_time)


class Week(Model):
    """A week. Each day has a boolean list of 24 hours."""

    monday = BooleanListField()
    tuesday = BooleanListField()
    wednesday = BooleanListField()
    thursday = BooleanListField()
    friday = BooleanListField()
    saturday = BooleanListField()
    sunday = BooleanListField()


class Term(Model):

    SEASONS = ['Fall', 'Winter', 'Spring', 'Summer']
    SEASON_CHOICES = [(SEASONS.index(season), season) for season in SEASONS]

    season_index = IntegerField(choices=SEASON_CHOICES)
    year = PositiveSmallIntegerField()
    schedule = ManyToManyField(Section, blank=True)
    preferences_lock_date = DateField()
    votes_lock_date = DateField()

    def __unicode__(self):
        return self.SEASONS[self.season_index] + " " + str(self.year)

    @property
    def preferences_locked(self):
        today = datetime.date.today()

        if today >= self.preferences_lock_date:
            return True

        return False

    @property
    def votes_locked(self):
        today = datetime.date.today()

        if today >= self.votes_lock_date:
            return True

        return False

    def get_or_create_current_term(self):
        today = datetime.date.today()

        # Convert date to month and day as integer (md), e.g. 4/21 = 421, 11/17 = 1117, etc.
        # See: http://stackoverflow.com/questions/16139306/determine-season-given-timestamp-in-python-using-datetime
        year = today.year
        month = today.month * 100
        day = today.day
        monthday = month + day

        if monthday >= 921 and monthday <= 1231:
            season = self.SEASONS.index("Fall")
            lock_date = datetime.date(year, 11, 1)
        elif monthday >= 11 and monthday <= 320:
            season = self.SEASONS.index("Winter")
            lock_date = datetime.date(year, 2, 1)
        elif monthday >= 321 and monthday <= 620:
            season = self.SEASONS.index("Spring")
            lock_date = datetime.date(year, 5, 1)
        elif monthday >= 621 and monthday <= 920:
            season = self.SEASONS.index("Summer")
            lock_date = datetime.date(year, 8, 1)
        else:
            season = None
            lock_date = None

        if season:
            try:
                term = Term.objects.get(season_index=season, year=year)
            except Term.DoesNotExist:
                new_term = Term(season_index=season, year=year)
                new_term.votes_lock_date = lock_date
                new_term.preferences_lock_date = lock_date
                new_term.save()

                term = new_term

        return term

    class Meta:
        unique_together = ("season_index", "year")

"""
.. module:: poly_schedules.preferences.views
   :synopsis: Poly Schedules Preferences Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from datetime import time

from django.views.generic.base import TemplateView

from ..schedules.models import Course, Term
from .forms import CoursePreferenceForm
from .models import CoursePreference


DAY_START = 7
DAY_END = 22


class PreferencesView(TemplateView):
    """Displays an instructors's course and time preferences."""

    template_name = "preferences/preferences.html"

    def get(self, *args, **kwargs):
        # Create user preferences if they don't exist.
        self.request.user.initialize_preferences()

        return super(PreferencesView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PreferencesView, self).get_context_data(**kwargs)

        availability_rows = []
        course_preference_list = []

        current_term = Term().get_or_create_current_term()

        availability = self.request.user.time_preference.get(term=current_term).availability

        # Build availability rows
        for hour in xrange(24):
            if hour >= DAY_START and hour <= DAY_END:
                list_object = {}
                list_object["hour"] = hour
                list_object["time"] = time(hour)

                for day in availability._meta.fields:
                    if not day.primary_key:
                        list_object[day.name] = getattr(availability, day.name)[hour]

                availability_rows.append(list_object)

        # Build a list of courses
        for course in Course.objects.all():
            preference = CoursePreference.objects.get(term=Term().get_or_create_current_term(), course=course)

            list_object = {}
            list_object['course'] = course
            list_object['preference_form'] = CoursePreferenceForm(instance=preference)

            course_preference_list.append(list_object)

        context['availability_rows'] = availability_rows
        context['course_preference_list'] = course_preference_list

        return context

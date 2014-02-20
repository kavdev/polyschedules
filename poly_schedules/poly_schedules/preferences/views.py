"""
.. module:: poly_schedules.preferences.views
   :synopsis: Poly Schedules Preferences Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.views.generic.base import TemplateView

from schedules.models import Course
from preferences.forms import CoursePreferenceForm


class PreferencesView(TemplateView):
    """Displays an instructors's course and time preferences."""

    template_name = "preferences/preferences.html"

    def get_context_data(self, **kwargs):
        course_preference_list = []

        for course in Course.objects.all():
            preference_form = CoursePreferenceForm(instance=course)

            list_object = {}
            list_object.add(course)
            list_object.add(preference_form)

            course_preference_list.append(list_object)

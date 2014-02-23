"""
.. module:: poly_schedules.preferences.views
   :synopsis: Poly Schedules Preferences Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.views.generic.base import TemplateView

from schedules.models import Course, Term
from .forms import CoursePreferenceForm
from .models import CoursePreference


class PreferencesView(TemplateView):
    """Displays an instructors's course and time preferences."""

    template_name = "preferences/preferences.html"

    def get(self, *args, **kwargs):
        # Create user preferences if they don't exist.
        self.request.user.initialize_preferences()

        return super(PreferencesView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PreferencesView, self).get_context_data(**kwargs)

        course_preference_list = []

        # Build a list of courses
        for course in Course.objects.all():
            preference = CoursePreference.objects.get(term=Term().get_or_create_current_term(), course=course)

            list_object = {}
            list_object['course'] = course
            list_object['preference_form'] = CoursePreferenceForm(instance=preference)

            course_preference_list.append(list_object)

        context['course_preference_list'] = course_preference_list
        return context

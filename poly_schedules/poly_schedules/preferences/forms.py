"""
.. module:: poly_schedules.preferences.forms
   :synopsis: Poly Schedules Preference Forms.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.forms import ModelForm
from django.forms.widgets import RadioSelect

from ..preferences.models import CoursePreference


class CoursePreferenceForm(ModelForm):

    class Meta:
        model = CoursePreference
        fields = ('preference', )
        widgets = {
            'preference': RadioSelect(),
        }

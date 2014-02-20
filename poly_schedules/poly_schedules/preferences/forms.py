"""
.. module:: poly_schedules.preferences.forms
   :synopsis: Poly Schedules Preference Forms.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.forms import ModelForm
from django.forms.widgets import RadioSelect

from preferences.models import CoursePreference


class CoursePreferenceForm(ModelForm):

    model = CoursePreference

    def __init__(self, *args, **kwargs):
        super(CoursePreferenceForm, self).__init__(*args, **kwargs)
        self.fields['availability'].widget = RadioSelect

    class Meta:
        fields = ('availability', )

"""
.. module:: poly_schedules.core.forms
   :synopsis: Poly Schedules Core Forms.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""


from django.forms import Form, ModelChoiceField

from ..schedules.models import Term


class TermDropdownForm(Form):

    term = ModelChoiceField(queryset=Term.objects.all(), label='', empty_label=None)

    def __init__(self, term_id, *args, **kwargs):
        super(TermDropdownForm, self).__init__(*args, **kwargs)

        self.fields["term"].initial = term_id

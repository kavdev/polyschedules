"""
.. module:: poly_schedules.core.context_processors
   :synopsis: Poly Schedules Core Context Processors.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from .forms import TermDropdownForm
from poly_schedules.schedules.models import Term


def term_dropdown(request):
    """Adds the term dropdown choices to each context request."""

    extra_context = {}
    extra_context['term'] = Term().get_or_create_current_term()
    extra_context['term_form'] = TermDropdownForm()

    return extra_context

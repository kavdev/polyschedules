"""
.. module:: poly_schedules.core.context_processors
   :synopsis: Poly Schedules Core Context Processors.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from .forms import TermDropdownForm


def term_dropdown(request):
    """Adds the term dropdown choices to each context request."""

    extra_context = {}
    extra_context['term_form'] = TermDropdownForm()

    return extra_context

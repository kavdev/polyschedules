"""
.. module:: poly_schedules.core.context_processors
   :synopsis: Poly Schedules Core Context Processors.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from .forms import TermDropdownForm


def term_dropdown(request):
    """Adds the term dropdown choices to each context request."""

    extra_context = {}

    if 'term_id' in request.session:
        extra_context['term_form'] = TermDropdownForm(term_id=request.session['term_id'])

    return extra_context

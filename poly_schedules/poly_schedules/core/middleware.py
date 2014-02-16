"""
.. module:: poly_schedules.core.middleware
   :synopsis: Poly Schedules Core Middleware.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.cache import cache

from schedules.models import Term
from .forms import TermDropdownForm


class TermMiddleware(object):
    """Adds the term dropdown choices to each request and sets the current term."""

    def process_request(self, request):
        term_cache_key = 'CurrentTerm'
        term = cache.get(term_cache_key)

        if not term:
            term_instance = Term()
            term = term_instance.get_current_term()

        term_form = TermDropdownForm()

        request.term = term
        request.term_form = term_form

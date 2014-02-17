"""
.. module:: poly_schedules.core.views
   :synopsis: Poly Schedules Core Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import ldap

from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect


class LoginView(FormView):
    """Displays the login form and handles the login action."""

    template_name = 'core/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):

        # Authenticate the user against LDAP
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user.is_authenticated():
            auth_login(self.request, user)

        return super(LoginView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['server_down'] = False

        # Make sure the auth server is available
        server = settings.AUTH_LDAP_SERVER_URI
        con = ldap.initialize(server)

        try:
            con.simple_bind()
        except ldap.SERVER_DOWN:
            context['server_down'] = True

        return context


def logout(request):
    """Logs the current user out."""

    auth_logout(request)
    redirection = reverse_lazy('home')
    return HttpResponseRedirect(redirection)


def handler500(request):
    """500 error handler which includes ``request`` in the context."""

    from django.template import Context, loader
    from django.http import HttpResponseServerError

    template = loader.get_template('500.html')

    return HttpResponseServerError(template.render(Context({'request': request, 'STATIC_URL': settings.STATIC_URL})))

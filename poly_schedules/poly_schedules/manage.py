#!/usr/bin/env python
import os
import sys

from colorama import init as color_init
from colorama import Fore, Style
from unipath import Path


def activate_env():
    """ Activates the virtual environment for this project."""

    error_msg = None

    try:
        virtualenv_dir = Path(os.environ['WORKON_HOME'])
    except KeyError:
        error_msg = "Error: 'WORKON_HOME' is not set."

    if error_msg:
        color_init()
        sys.stderr.write(Fore.RED + Style.BRIGHT + error_msg + "\n")
        sys.exit(1)

    filepath = Path(__file__).absolute()
    site_dir = filepath.ancestor(4).components()[-1]

    # Add the app's directory to the PYTHONPATH
    sys.path.append(filepath.ancestor(2))
    sys.path.append(filepath.ancestor(1))

    # Set manually in environment
    #os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

    # Activate the virtual env
    activate_env = virtualenv_dir.child(site_dir, "bin", "activate_this.py")
    execfile(activate_env, dict(__file__=activate_env))

if __name__ == "__main__":

    # Set this manually in the environment...
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")

    color_init()
    activate_env()

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        sys.stderr.write(Fore.RED + Style.BRIGHT + "Error: Django could not be imported - please make sure it is installed.\nIf you are using a Virtual Environment, please make sure it is activated.\n\n")
        sys.exit(1)

    execute_from_command_line(sys.argv)

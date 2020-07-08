"""The generic views for the eox-hooks plugin project.

Methods:
    info_view: Show basic plugin information.
"""
from __future__ import unicode_literals

from os.path import dirname, realpath
from subprocess import CalledProcessError, check_output

from django.http import JsonResponse

import eox_hooks


def info_view(request):  # pylint: disable=unused-argument
    """Show basic current plugin information.

    This view allows to identify the current plugin version per
    instance by returning the version number or git commit identifier.

    Returns:
        A dict mapping keys to the corresponding plugin version, name and git commit.
        Example:

        {
            'version': 2.5.4,
            'name': 'eox-hooks',
            'git': 7862374283974923654,
        }
    """
    try:
        working_dir = dirname(realpath(__file__))
        git_data = check_output(['git', 'rev-parse', 'HEAD'], cwd=working_dir)
        git_data = git_data.decode().rstrip('\r\n')
    except CalledProcessError:
        git_data = ''

    return JsonResponse(
        {
            'version': eox_hooks.__version__,
            'name': 'eox-hooks',
            'git': git_data,
        },
    )

# -*- coding: utf-8 -*-
"""Exceptions and warnings for :mod:`pytan3.api_clients`."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions


class ModuleError(exceptions.PyTanError):
    """Parent of all exceptions for :mod:`pytan3.api_clients`.

    Thrown by:
      * :func:`pytan3.api_clients.load_type`
      * :func:`pytan3.api_clients.load`

    """

    pass


class ModuleWarning(exceptions.PyTanWarning):
    """Parent of all warnings for :mod:`pytan3.api_clients`.

    Thrown by:

    """

    pass


class GetPlatformVersionWarning(ModuleWarning):
    """Thrown when an issue happens while trying to get the platform version.

    Thrown by:
      * :func:`pytan3.api_clients.get_version`

    """

    pass

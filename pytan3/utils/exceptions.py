# -*- coding: utf-8 -*-
"""Exceptions and warnings for :mod:`pytan3.utils`."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions


class ModuleError(exceptions.PyTanError):
    """Parent of all exceptions for :mod:`pytan3.utils`.

    Thrown by:
      * :func:`pytan3.utils.logs.level_name`
      * :func:`pytan3.utils.logs.level_int`

    """

    pass


class ModuleWarning(exceptions.PyTanWarning):
    """Parent of all warnings for :mod:`pytan3.utils`.

    Thrown by:

    """

    pass


class VersionMismatchError(ModuleError):
    """Exception handler when matching a version.

    Thrown from:
      * :func:`pytan3.utils.versions.version_check_obj_req`

    """

    pass

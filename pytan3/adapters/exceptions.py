# -*- coding: utf-8 -*-
"""Exceptions and warnings for :mod:`pytan3.adapters`."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions


class ModuleError(exceptions.PyTanError):
    """Parent of all exceptions for :mod:`pytan3.adapters`.

    Thrown by:
      * :func:`pytan3.adapters.load_type`
      * :func:`pytan3.adapters.load`

    """

    pass


class ModuleWarning(exceptions.PyTanWarning):
    """Parent of all warnings for :mod:`pytan3.adapters`.

    Thrown by:

    """

    pass


class InvalidTypeError(ModuleError):
    """Thrown when an object of an invalid type is supplied.

    Thrown by:
      * :func:`pytan3.adapters.Adapter.api_get_audit_logs`
      * :func:`pytan3.adapters.check_object_type`

    """

    pass


class EmptyAttributeError(ModuleError):
    """Thrown when an object is supplied that does not have required attributes set.

    Thrown by:
      * :func:`pytan3.adapters.check_object_attrs`

    """

    pass


class TypeMismatchError(ModuleError):
    """Thrown when an API module type does not match an adapters type.

    Thrown by:
      * :func:`pytan3.adapters.check_adapter_types`

    """

    pass


class SessionNotFoundWarning(ModuleWarning):
    """Thrown when a session XML tag can not be found in a response body.

    Thrown by:
      * :func:`pytan3.adapters.Soap.send`

    """

    pass

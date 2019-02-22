# -*- coding: utf-8 -*-
"""Exceptions and warnings for :mod:`pytan3.http_client`."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions


class ModuleError(exceptions.PyTanError):
    """Parent of all exceptions for :mod:`pytan3.http_client`.

    Thrown by:
      * :meth:`pytan3.http_client.UrlParser.__init__`

    """

    pass


class ModuleWarning(exceptions.PyTanWarning):
    """Parent of all warnings for :mod:`pytan3.http_client`.

    Thrown by:

    """

    pass


class CertificateNotFoundWarning(ModuleWarning):
    """Thrown when a cert can not be found.

    Thrown by:
      * :meth:`pytan3.http_client.Certify.__call__`

    """

    pass


class CertificateInvalidError(ModuleError):
    """Thrown when cert is invalid from path or from user prompt.

    Thrown by:
      * :meth:`pytan3.http_client.Certify.verify_hook`
      * :meth:`pytan3.http_client.Certify.check_path`

    """

    pass

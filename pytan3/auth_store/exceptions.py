# -*- coding: utf-8 -*-
"""Exceptions and warnings for :mod:`pytan3.auth_store`."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions


class ModuleError(exceptions.PyTanError):
    """Parent of all :obj:`pytan3.auth_store` exceptions.

    Thrown by:
      * :meth:`pytan3.auth_store.AuthStore.get`
      * :meth:`pytan3.auth_store.AuthStore.to_path`
      * :meth:`pytan3.auth_store.AuthStore.from_path`

    """

    pass


class ModuleWarning(exceptions.PyTanWarning):
    """Parent of all :obj:`pytan3.auth_store` warnings.

    Thrown by:
      * :meth:`pytan3.auth_store.AuthStore.to_path`

    """

    pass

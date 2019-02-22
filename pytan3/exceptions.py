# -*- coding: utf-8 -*-
"""Parent exceptions and warnings for the PyTan package."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class PyTanError(Exception):
    """Parent exception for all :mod:`pytan3` errors."""

    pass


class PyTanWarning(Warning):
    """Parent warning for all :mod:`pytan3` warnings."""

    pass

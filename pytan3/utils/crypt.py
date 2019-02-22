# -*- coding: utf-8 -*-
"""PyTan encryption/decryption utilities module."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six

import privy
from . import exceptions


def encrypt(data, key):
    """Encrypt data with key using privy.

    Args:
        data (:obj:`str`):
            Data to encrypt with key.
        key (:obj:`str`):
            Key to encrypt data with.

    Returns:
        :obj:`str`

    """
    data = six.ensure_binary(data)
    data = privy.hide(secret=data, password=key)
    data = six.ensure_text(data)
    return data


def decrypt(data, key):
    """Decrypt data with key using privy.

    Args:
        data (:obj:`str`):
            Data to decrypt with key.
        key (:obj:`str`):
            Key data was encrypted with.

    Raises:
        :exc:`pytan3.utils.exceptions.ModuleError`:
            On ValueError from privy when decryption fails.

    Returns:
        :obj:`str`

    """
    data = six.ensure_binary(data)
    try:
        data = privy.peek(hidden=data, password=key)
    except ValueError:
        error = "Unable to decrypt {cnt} bytes of data using key {k}, invalid key!"
        error = error.format(cnt=len(data), k=key)
        raise exceptions.ModuleError(error)
    return six.ensure_text(data)

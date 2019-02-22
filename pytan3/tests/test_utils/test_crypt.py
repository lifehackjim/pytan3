# -*- coding: utf-8 -*-
"""Test suite for pytan3."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import pytan3
import re


def test_encrypt_decrypt():
    """Test encrypt / decrypt with valid key."""
    data = "{}#!:What a lame test"
    key = "An even lamer key"
    crypt = pytan3.utils.crypt.encrypt(data=data, key=key)
    assert re.match(r"\d+\$\d+\$", crypt)
    back = pytan3.utils.crypt.decrypt(data=crypt, key=key)
    assert back == data


def test_decrypt_bad_key():
    """Test exc thrown with bad key."""
    data = "{}#!:What a lame test"
    key = "An even lamer key"
    crypt = pytan3.utils.crypt.encrypt(data=data, key=key)
    with pytest.raises(pytan3.utils.exceptions.ModuleError):
        pytan3.utils.crypt.decrypt(data=crypt, key="an even worse key")

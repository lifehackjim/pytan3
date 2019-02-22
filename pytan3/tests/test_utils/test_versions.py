# -*- coding: utf-8 -*-
"""Test suite for pytan3."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytan3


def test_version_max_false():
    """Test versions that are higher than they should be return False."""
    check = pytan3.utils.versions.version_max(v1="9", v2="7")
    assert check is False
    check = pytan3.utils.versions.version_max(v1="9.9", v2="7")
    assert check is False
    check = pytan3.utils.versions.version_max(v1="9.9", v2="7.2")
    assert check is False
    check = pytan3.utils.versions.version_max(v1="9.9", v2="7.2.314")
    assert check is False
    check = pytan3.utils.versions.version_max(v1="9.9", v2="7.2.314.4313")
    assert check is False
    check = pytan3.utils.versions.version_max(v1="9.9.9", v2="7.2.314.4313")
    assert check is False


def test_version_max_true():
    """Test versions that are not higher than they should be return True."""
    check = pytan3.utils.versions.version_max(v1="6", v2="7")
    assert check is True
    check = pytan3.utils.versions.version_max(v1="6.8", v2="7")
    assert check is True
    check = pytan3.utils.versions.version_max(v1="6.8.4", v2="7")
    assert check is True
    check = pytan3.utils.versions.version_max(v1="6.8.4.4", v2="7")
    assert check is True
    check = pytan3.utils.versions.version_max(v1="7.1", v2="7.1")
    assert check is True
    check = pytan3.utils.versions.version_max(v1="7.1.2", v2="7.1")
    assert check is True
    check = pytan3.utils.versions.version_max(v1="7.1.2.a", v2="7.1.2")
    assert check is True
    check = pytan3.utils.versions.version_max(v1="7.1.2.a", v2="7.1.2")
    assert check is True


def test_version_max_shrink_false():
    """Test shrunk versions that are higher than they should be return False."""
    check = pytan3.utils.versions.version_max(v1="7.8.1.2", v2="7.7.2.3", vshrink=2)
    assert check is False
    check = pytan3.utils.versions.version_max(v1="7.8.1.2", v2="7.7.2", vshrink=True)
    assert check is False
    check = pytan3.utils.versions.version_max(v1="7.8.1.2", v2="7.7", vshrink=True)
    assert check is False


def test_version_max_shrink_true():
    """Test shrunk versions that are not higher than they should be return True."""
    check = pytan3.utils.versions.version_max(v1="7.8.1.2", v2="7.7.2.3", vshrink=1)
    assert check is True
    check = pytan3.utils.versions.version_max(v1="7.8.1.2", v2="7", vshrink=True)
    assert check is True
    check = pytan3.utils.versions.version_max(v1="7.6.1.2", v2="7.7", vshrink=True)
    assert check is True
    check = pytan3.utils.versions.version_max(v1="7.6.1.2", v2="7.6.1", vshrink=True)
    assert check is True


def test_version_min_false():
    """Test versions that are lower than they should be return False."""
    check = pytan3.utils.versions.version_min(v1="7", v2="9")
    assert check is False
    check = pytan3.utils.versions.version_min(v1="7", v2="9.9")
    assert check is False
    check = pytan3.utils.versions.version_min(v1="7.2", v2="9.9")
    assert check is False
    check = pytan3.utils.versions.version_min(v1="7.2.314", v2="9.9")
    assert check is False
    check = pytan3.utils.versions.version_min(v1="7.2.314.4313", v2="9.9")
    assert check is False
    check = pytan3.utils.versions.version_min(v1="7.2.314.4313", v2="9.9.9")
    assert check is False


def test_version_min_true():
    """Test versions that are not lower than they should be return True."""
    check = pytan3.utils.versions.version_min(v1="7", v2="6")
    assert check is True
    check = pytan3.utils.versions.version_min(v1="7", v2="6.8")
    assert check is True
    check = pytan3.utils.versions.version_min(v1="7", v2="6.8.4")
    assert check is True
    check = pytan3.utils.versions.version_min(v1="7", v2="6.8.4.4")
    assert check is True
    check = pytan3.utils.versions.version_min(v1="7.1", v2="7.1")
    assert check is True
    check = pytan3.utils.versions.version_min(v1="7.1.3", v2="7.1.2")
    assert check is True
    check = pytan3.utils.versions.version_min(v1="7.1.2.a", v2="7.1.2")
    assert check is True


def test_version_min_shrink_false():
    """Test shrunk versions that are lower than they should be return False."""
    check = pytan3.utils.versions.version_min(v1="7.8.1.2", v2="7.9.2.3", vshrink=2)
    assert check is False
    check = pytan3.utils.versions.version_min(v1="7.8.1.2", v2="7.9.2", vshrink=True)
    assert check is False
    check = pytan3.utils.versions.version_min(v1="7.8.1.2", v2="7.9", vshrink=True)
    assert check is False


def test_version_min_shrink_true():
    """Test shrunk versions that are not lower than they should be return True."""
    check = pytan3.utils.versions.version_min(v1="7.8.1.2", v2="7.7.2.3", vshrink=1)
    assert check is True
    check = pytan3.utils.versions.version_min(v1="7.8.1.2", v2="7", vshrink=True)
    assert check is True
    check = pytan3.utils.versions.version_min(v1="7.8.1.2", v2="7.8", vshrink=True)
    assert check is True
    check = pytan3.utils.versions.version_min(v1="7.8.1.2", v2="7.8.1", vshrink=True)
    assert check is True


def test_version_eq_false():
    """Test versions that are not equal return False."""
    check = pytan3.utils.versions.version_eq(v1="8", v2="7.2")
    assert check is False
    check = pytan3.utils.versions.version_eq(v1="8", v2="7")
    assert check is False
    check = pytan3.utils.versions.version_eq(v1="7.1.2.3", v2="7.2")
    assert check is False
    check = pytan3.utils.versions.version_eq(v1="7.1.2.3", v2="7.1.3")
    assert check is False
    check = pytan3.utils.versions.version_eq(v1="7.1.2.3", v2="7.1.2.4")
    assert check is False


def test_version_eq_true():
    """Test versions that are equal return True."""
    check = pytan3.utils.versions.version_eq(v1="7.1.2.a", v2="7.1.2")
    assert check is True
    check = pytan3.utils.versions.version_eq(v1="7.1.2.a", v2="7.1.2.a")
    assert check is True
    check = pytan3.utils.versions.version_eq(v1="7", v2="7")
    assert check is True
    check = pytan3.utils.versions.version_eq(v1="7.1.2.3", v2="7")
    assert check is True
    check = pytan3.utils.versions.version_eq(v1="7.1.2.3", v2="7.1")
    assert check is True
    check = pytan3.utils.versions.version_eq(v1="7.1.2.3", v2="7.1.2")
    assert check is True
    check = pytan3.utils.versions.version_eq(v1="7.1.2.3", v2="7.1.2.3")
    assert check is True


def test_version_eq_shrink_false():
    """Test shrunk versions that are not equal return False."""
    check = pytan3.utils.versions.version_eq(v1="7.8.1.2", v2="7.9.2.3", vshrink=2)
    assert check is False
    check = pytan3.utils.versions.version_eq(v1="7.8.1.2", v2="8", vshrink=True)
    assert check is False
    check = pytan3.utils.versions.version_eq(v1="7.8.1.2", v2="7.9", vshrink=True)
    assert check is False
    check = pytan3.utils.versions.version_eq(v1="7.8.1.2", v2="7.8.2", vshrink=True)
    assert check is False


def test_version_eq_shrunk_true():
    """Test shrunk versions that are equal return True."""
    check = pytan3.utils.versions.version_eq(v1="7.8.1.2", v2="7.7.2.3", vshrink=1)
    assert check is True
    check = pytan3.utils.versions.version_eq(v1="7.8.1.2", v2="7", vshrink=True)
    assert check is True
    check = pytan3.utils.versions.version_eq(v1="7.8.1.2", v2="7.8", vshrink=True)
    assert check is True
    check = pytan3.utils.versions.version_eq(v1="7.8.1.2", v2="7.8.1", vshrink=True)
    assert check is True
    check = pytan3.utils.versions.version_eq(v1="7.8.1.2", v2="7.8.1.2", vshrink=True)
    assert check is True


def test_version_check_false():
    """Test various combos that should be false."""
    check = pytan3.utils.versions.version_check(
        version="7.2.3.4", veq="7", vmax="6", vshrink=True
    )
    assert check is False

    check = pytan3.utils.versions.version_check(
        version="7.2.3.4", veq="7", vmax="8", vmin="8", vshrink=True
    )
    assert check is False

    check = pytan3.utils.versions.version_check(
        version="7", veq="7.2", vmax="8", vmin="6", vshrink=True
    )
    assert check is False

    check = pytan3.utils.versions.version_check(
        version="7.1.2.3", veq="7", vshrink=False
    )
    assert check is False


def test_version_check_true():
    """Test various combos that should be true."""
    check = pytan3.utils.versions.version_check(
        version="7.2.3.4", veq="7", vmax="8", vmin="6", vshrink=True
    )
    assert check is True

    check = pytan3.utils.versions.version_check(
        version="7", veq="7.2", vmax="8.3", vmin="6.2", vshrink=1
    )
    assert check is True

    check = pytan3.utils.versions.version_check(
        version="7.2.3", veq="7.2", vmax="8", vmin="6", vshrink=True
    )
    assert check is True

    check = pytan3.utils.versions.version_check(
        version="7.1.2.3", vmin="7", vshrink=True
    )
    assert check is True

    check = pytan3.utils.versions.version_check(
        version="7.1.2.3", vmin="7", vshrink=False
    )
    assert check is True

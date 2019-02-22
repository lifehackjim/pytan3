# -*- coding: utf-8 -*-
"""Test suite for pytan3."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytan3
import os
import datetime
import pytest
import six
import time


def test_get_env_empty():
    """Test empty environment variable returns the default value."""
    assert pytan3.utils.tools.get_env(key="abc", default="moo") == "moo"


def test_get_env_set():
    """Test set environment variable returns the set value."""
    os.environ["abc"] = "new moo"
    assert pytan3.utils.tools.get_env(key="abc", default="moo") == "new moo"


def test_get_storage_dir_default():
    """Test default storage dir has _local in it and path does not exist."""
    x = pytan3.utils.tools.get_storage_dir()
    assert pytan3.utils.tools.STORAGE_DIR in format(x)


def test_get_storage_dir_default_sub():
    """Test default storage dir has _local in it and path does not exist."""
    x = pytan3.utils.tools.get_storage_dir(path_sub="merp")
    assert format(x).endswith("merp")
    assert not os.path.exists(format(x))


def test_get_storage_dir_custom_mkdir(tmp_path):
    """Test creating a dir."""
    x = pytan3.utils.tools.get_storage_dir(
        path=tmp_path / "foo", path_sub="merp", mkdir=True
    )
    assert os.path.exists(format(x))
    assert format(x).endswith("merp")


def test_secs():
    """Test int and delta return datetime obj."""
    x = pytan3.utils.tools.secs_ago(5)
    y = pytan3.utils.tools.secs_age(x)
    assert isinstance(x, datetime.datetime)
    assert y == 5


def test_b64():
    """Test b64 encode and decode both work."""
    x = pytan3.utils.tools.b64_encode("moo")
    y = pytan3.utils.tools.b64_decode(x)
    assert y == "moo"


def test_trim_txt():
    """Test text gets trimmed properly."""
    x = "n" * 9999
    assert len(pytan3.utils.tools.trim_txt(x)) == 9999
    x += "o" * 50
    assert len(pytan3.utils.tools.trim_txt(x)) == 10034


def test_get_dict_path_bad():
    """Test invalid paths throw exc."""
    d = {"a": {"b": {"c": "d", "e": [1, 2, 3]}}}
    with pytest.raises(ValueError):
        pytan3.utils.tools.get_dict_path(obj=d, path="")
    with pytest.raises(ValueError):
        pytan3.utils.tools.get_dict_path(obj=d, path="/x")
    with pytest.raises(ValueError):
        pytan3.utils.tools.get_dict_path(obj=d, path="/a/b/e/f")


def test_get_dict_path():
    """Test valid paths work."""
    d = {"a": {"b": {"c": "d", "e": [1, 2, 3]}}}
    x = pytan3.utils.tools.get_dict_path(obj=d, path="/a")
    assert x == {"b": {"c": "d", "e": [1, 2, 3]}}
    x = pytan3.utils.tools.get_dict_path(obj=d, path="a")
    assert x == {"b": {"c": "d", "e": [1, 2, 3]}}
    x = pytan3.utils.tools.get_dict_path(obj=d, path="/a/b")
    assert x == {"c": "d", "e": [1, 2, 3]}
    x = pytan3.utils.tools.get_dict_path(obj=d, path="/a/b/c/")
    assert x == "d"


def test_human_size():
    """Test int and str return proper format."""
    assert pytan3.utils.tools.human_size("100000") == "100 KB"
    assert pytan3.utils.tools.human_size(100000) == "100 KB"


def test_human_delta_timedelta():
    """Test timedelta obj produces proper format."""
    delta = datetime.timedelta(seconds=301, microseconds=6000)
    assert pytan3.utils.tools.human_delta(delta) == "5m1.01s"


def test_human_delta_timedelta_ms():
    """Test timedelta obj produces proper format."""
    delta = datetime.timedelta(seconds=300, microseconds=6000)
    assert pytan3.utils.tools.human_delta(delta, ms=True) == "5m6ms"


def test_human_delta_str():
    """Test timedelta obj produces proper format."""
    assert pytan3.utils.tools.human_delta("300.4") == "5m0.4s"


def test_human_delta_datetime():
    """Test timedelta obj produces proper format."""
    assert pytan3.utils.tools.human_delta(datetime.datetime.utcnow()) == "0s"


def test_human_delta_str_ms():
    """Test timedelta obj produces proper format."""
    assert pytan3.utils.tools.human_delta("301.4", ms=True) == "5m1s400ms"


def test_human_delta_str_ms_not_short():
    """Test timedelta obj produces proper format."""
    exp = "5 minutes, 1 second and 400 milliseconds"
    assert pytan3.utils.tools.human_delta("301.4", ms=True, short=False) == exp


def test_human_delta_falsey():
    """Test timedelta obj produces proper format."""
    assert pytan3.utils.tools.human_delta(None) == "0s"
    assert pytan3.utils.tools.human_delta(0) == "0s"
    assert pytan3.utils.tools.human_delta(False) == "0s"


def test_timer():
    """Test formatting comes out right."""
    with pytan3.utils.tools.Timer() as t:
        time.sleep(0.01)
        assert isinstance(t.elapsed, six.string_types)
    assert "ms" in format(t)
    assert "ms" in repr(t)
    assert isinstance(format(t), six.string_types)
    assert isinstance(t.elapsed, six.string_types)
    assert isinstance(t.elapsed_int, int)
    assert isinstance(t.elapsed_delta, datetime.timedelta)


def test_timer_exc():
    """Test exception doesnt get swallowd."""
    with pytest.raises(Exception):
        with pytan3.utils.tools.Timer():
            raise Exception()


def test_str_to_intfloat():
    """Test str gets converted to int or float properly."""
    check = pytan3.utils.tools.str_to_intfloat("0.3")
    assert isinstance(check, float)
    check = pytan3.utils.tools.str_to_intfloat("3")
    assert isinstance(check, int)

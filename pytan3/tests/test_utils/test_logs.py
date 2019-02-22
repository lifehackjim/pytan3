# -*- coding: utf-8 -*-
"""Test suite for pytan3."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import warnings
import pytan3
import sys
import logging
import time
import pytest
import os
import io


def test_custom_warning():
    """Pass."""
    pytan3.utils.logs.disable_format_warning()
    assert warnings.formatwarning == pytan3.utils.logs._formatwarning
    pytan3.utils.logs.enable_format_warning()
    z = pytan3.utils.logs.customformatwarning(
        "x", pytan3.exceptions.PyTanWarning, __name__, 3
    )
    assert "!!!" in z
    assert warnings.formatwarning == pytan3.utils.logs.customformatwarning


def test_log_is_enabled():
    """Test log enabled check works."""
    log = pytan3.LOG.getChild("log1")
    assert pytan3.utils.logs.is_enabled(obj=log) is True


def test_log_is_disabled():
    """Test log disabled check works."""
    log = pytan3.LOG.getChild("log2")
    log.disabled = True
    assert pytan3.utils.logs.is_disabled(obj=log) is True


def test_log_is_disabled_child():
    """Test log disabled check works on child when parent disabled."""
    log1 = pytan3.LOG.getChild("log3")
    log2 = log1.getChild("log4")
    assert pytan3.utils.logs.is_disabled(obj=log2) is False
    log1.disabled = True
    assert pytan3.utils.logs.is_disabled(obj=log2) is True


def test_log_capture_exc():
    """Test enable/disable capture exc."""
    pytan3.utils.logs.disable_capture_exc()
    assert sys.excepthook == pytan3.utils.logs._sys_excepthook
    pytan3.utils.logs.enable_capture_exc()
    assert sys.excepthook == pytan3.utils.logs.exception_hook


def test_log_capture_warn():
    """Test enable/disable capture warn."""
    pytan3.utils.logs.disable_capture_warn()
    assert warnings.showwarning == pytan3.utils.logs._warnings_showwarning
    pytan3.utils.logs.enable_capture_warn()
    assert warnings.showwarning == pytan3.utils.logs.warning_hook


def test_log_time_switch():
    """Test gmt / local time switch."""
    pytan3.utils.logs.use_localtime()
    assert logging.Formatter.converter == time.localtime
    pytan3.utils.logs.use_gmt()
    assert logging.Formatter.converter == time.gmtime


def test_log_set_level_str():
    """Test text level set works."""
    log1 = pytan3.LOG.getChild("log5")
    pytan3.utils.logs.set_level(lvl="info", obj=log1)
    assert log1.level == logging.INFO


def test_log_set_level_int():
    """Test text level set works."""
    log1 = pytan3.LOG.getChild("log6")
    pytan3.utils.logs.set_level(lvl=logging.DEBUG, obj=log1)
    assert log1.level == logging.DEBUG


def test_log_set_level_off():
    """Test level off disables logger."""
    log1 = pytan3.LOG.getChild("log7")
    pytan3.utils.logs.set_level(lvl="off", obj=log1)
    assert log1.disabled is True


def test_log_set_level_bad():
    """Test exc thrown on bad str/int levels."""
    log = pytan3.LOG.getChild("log8")
    with pytest.raises(pytan3.utils.exceptions.ModuleError):
        pytan3.utils.logs.set_level(lvl="bad", obj=log)
    with pytest.raises(pytan3.utils.exceptions.ModuleError):
        pytan3.utils.logs.set_level(lvl=69, obj=log)


def test_log_get_obj_log():
    """Test getting a logger for an object works."""
    log = pytan3.utils.logs.get_obj_log(pytan3.utils.prompts.promptness, lvl="info")
    assert log.name == "pytan3.utils.prompts.Promptness"
    assert log.level == logging.INFO


def test_log_level_name():
    """Test level name works for str/int."""
    lvl = pytan3.utils.logs.level_name(lvl=20)
    assert lvl == "INFO"
    lvl = pytan3.utils.logs.level_name(lvl="info")
    assert lvl == "INFO"


def test_log_level_name_bad():
    """Test exc thrown for bad level str/int."""
    with pytest.raises(pytan3.utils.exceptions.ModuleError):
        pytan3.utils.logs.level_name(lvl="bad")
    with pytest.raises(pytan3.utils.exceptions.ModuleError):
        pytan3.utils.logs.level_name(lvl=69)


def test_log_log_str():
    """Test log str works."""
    log = pytan3.LOG.getChild("log9")
    logstr = pytan3.utils.logs.log_str(obj=log)
    assert log.name in logstr
    assert "disabled=False" in logstr
    pytan3.utils.logs.add_null(log)
    assert "Null" not in logstr


def test_log_handler_str():
    """Test handler str works."""
    log = pytan3.LOG.getChild("log10")
    h = pytan3.utils.logs.add_stdout(obj=log)
    handler_str = pytan3.utils.logs.handler_str(obj=h)
    assert log.name in handler_str
    assert h.name in handler_str


def test_log_add_remove_stdout():
    """Test add/remove stdout."""
    log = pytan3.LOG.getChild("log11")
    h = pytan3.utils.logs.add_stdout(obj=log)
    assert h.name in [h.name for h in log.handlers]
    pytan3.utils.logs.remove_stdout(obj=log)
    assert h.name not in [h.name for h in log.handlers]


def test_log_add_remove_stderr():
    """Test add/remove stderr."""
    log = pytan3.LOG.getChild("log12")
    h = pytan3.utils.logs.add_stderr(obj=log)
    assert h.name in [h.name for h in log.handlers]
    h = pytan3.utils.logs.remove_stderr(obj=log)
    assert h.name not in [h.name for h in log.handlers]


def test_log_add_remove_file(tmp_path):
    """Test add/remove file logging."""
    path = tmp_path / "v"
    log = pytan3.LOG.getChild("log13")
    handler = pytan3.utils.logs.add_file(obj=log, path=path)
    assert handler.name in [h.name for h in log.handlers]
    log.debug("testabc")
    assert os.path.isfile(handler.name)
    pytan3.utils.logs.remove_file(obj=log, path=path)
    assert handler.name not in [h.name for h in log.handlers]
    contents = io.open(handler.name, "r").read()
    assert "testabc" in contents


def test_log_get_output_handlers():
    """Test get output handlers."""
    log = pytan3.LOG.getChild("log14")
    x = pytan3.utils.logs.get_output_handlers(obj=log, lvl="NOTSET")
    assert len(x) == 0
    h = pytan3.utils.logs.add_stderr(obj=log)
    x = pytan3.utils.logs.get_output_handlers(obj=log, lvl="INFO")
    assert len(x) >= 1
    assert h in x
    h = pytan3.utils.logs.add_null(obj=log)
    x = pytan3.utils.logs.get_output_handlers(obj=log, lvl="INFO")
    assert len(x) >= 1
    h = pytan3.utils.logs.add_stdout(obj=log)
    pytan3.utils.logs.set_level(obj=h, lvl="OFF")
    assert len(x) >= 1


def test_log_will_print_at():
    """Test will_print_at."""
    log = pytan3.LOG.getChild("log15")
    h = pytan3.utils.logs.add_stderr(obj=log)
    x = pytan3.utils.logs.will_print_at(obj=log, lvl="info")
    assert x is True
    pytan3.utils.logs.set_level(obj=log, lvl="OFF")
    x = pytan3.utils.logs.will_print_at(obj=log, lvl="debug")
    assert x is False
    pytan3.utils.logs.set_level(obj=h, lvl="error")
    x = pytan3.utils.logs.will_print_at(obj=log, lvl="debug")
    assert x is False

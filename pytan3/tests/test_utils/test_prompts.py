# -*- coding: utf-8 -*-
"""Test suite for pytan3."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytan3
import sys
import six
import input_mocker
import pytest


pytestmark = pytest.mark.skipif(
    sys.version_info < (3, 6), reason="requires python3.6 or higher"
)
# monkeypatch for isatty fails on 2.x, no time to figure it out


def notisatty():
    """Mock for tty."""
    return False


def isatty():
    """Mock for tty."""
    return True


def test_stdout_isatty(capsys):
    """Test stdout is a tty."""
    with capsys.disabled():
        assert pytan3.utils.prompts.isatty(sys.stdout) is True
    assert pytan3.utils.prompts.isatty(six.StringIO()) is False


def test_stream_isnotatty(capsys):
    """Test stream is not a tty."""
    assert pytan3.utils.prompts.isatty(six.StringIO()) is False


def test_stream_name(capsys):
    """Test stream name outputs proper str."""
    assert pytan3.utils.prompts.stream_name(six.StringIO()) == "StringIO"
    with capsys.disabled():
        assert pytan3.utils.prompts.stream_name(sys.stderr) == "<stderr>"


def test_str_repr():
    """Test stream name outputs proper str."""
    promptness = pytan3.utils.prompts.Promptness()
    assert "input=" in format(promptness)
    assert "output=" in format(promptness)
    assert "input=" in repr(promptness)
    assert "output=" in repr(promptness)


def test_prompt_notty_stderr(monkeypatch):
    """Test exc thrown when stderr is not a tty."""
    promptness = pytan3.utils.prompts.Promptness()
    with monkeypatch.context() as m:
        m.setattr("sys.stderr.isatty", notisatty)
        m.setattr("sys.stdin.isatty", isatty)
        v = promptness.prompt(text="text", default="moo")
        assert v == "moo"
        with pytest.raises(pytan3.utils.prompts.NoTtyError):
            promptness.prompt(text="text", default=None)


def test_prompt_notty_stdin(monkeypatch):
    """Test exc thrown when stdin is not a tty."""
    promptness = pytan3.utils.prompts.Promptness()
    with monkeypatch.context() as m:
        m.setattr("sys.stdin.isatty", notisatty)
        m.setattr("sys.stderr.isatty", isatty)
        v = promptness.prompt(text="text", default="moo")
        assert v == "moo"
        with pytest.raises(pytan3.utils.prompts.NoTtyError):
            promptness.prompt(text="text", default=None)


def test_choice_invalid_value_no_default(capsys, monkeypatch):
    """Test exc thrown when invalid choice provided with no default value."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = ["moo", "moo", "moo", "moo", "moo"]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            with pytest.raises(pytan3.utils.prompts.InvalidValueError):
                promptness.ask_choice(text="text", choices=["not", "a", "choice"])


def test_choice_empty_value_no_default(capsys, monkeypatch):
    """Test exc thrown when no choice provided with no default value."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = ["", "", "", "", ""]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            with pytest.raises(pytan3.utils.prompts.EmptyValueError):
                promptness.ask_choice(text="text", choices=["not", "a", "choice"])


def test_choice_empty_value_default(capsys, monkeypatch):
    """Test default choice used when no value provided."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = [""]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            v = promptness.ask_choice(
                text="text", choices=["Not", "a", "choice"], default="Not"
            )
            assert v == "Not"


def test_bool_invalid_value_no_default(capsys, monkeypatch):
    """Test exc thrown when invalid bool value provided."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = ["moo", "moo", "moo", "moo", "moo"]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            with pytest.raises(pytan3.utils.prompts.InvalidValueError):
                promptness.ask_bool(text="text")


def test_bool_empty_value_no_default(capsys, monkeypatch):
    """Test exc thrown when no bool value provided with no default value."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = ["", "", "", "", ""]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            with pytest.raises(pytan3.utils.prompts.EmptyValueError):
                promptness.ask_bool(text="text")


def test_bool_empty_value_default(capsys, monkeypatch):
    """Test default bool value used when no value provided."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = [""]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            v = promptness.ask_bool(text="text", default=True)
            assert v is True


def test_bool_value(capsys, monkeypatch):
    """Test valid bool value."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = ["y"]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            v = promptness.ask_bool(text="text")
            assert v is True


def test_int_invalid_value_no_default(capsys, monkeypatch):
    """Test exc thrown with invalid int value."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = ["moo", "moo", "moo", "moo", "moo"]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            with pytest.raises(pytan3.utils.prompts.InvalidValueError):
                promptness.ask_int(text="text")


def test_int_empty_value_no_default(capsys, monkeypatch):
    """Test exc thrown with no int provided with no default."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = ["", "", "", "", ""]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            with pytest.raises(pytan3.utils.prompts.EmptyValueError):
                promptness.ask_int(text="text")


def test_int_empty_value_default(capsys, monkeypatch):
    """Test default int value used when no value provided."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = [""]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            v = promptness.ask_int(text="text", default=23)
            assert v == 23


def test_int_value(capsys, monkeypatch):
    """Test valid int value works."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = ["23"]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            v = promptness.ask_int(text="text")
            assert v == 23


def test_str_empty_value_no_default(capsys, monkeypatch):
    """Test exc thrown no str value provided."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = [""]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            with pytest.raises(pytan3.utils.prompts.EmptyValueError):
                promptness.ask_str(text="text")


def test_str_invalid(capsys, monkeypatch):
    """Test exc thrown when invalid value supplied."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = ["xyz"]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            with pytest.raises(pytan3.utils.prompts.InvalidValueError):
                promptness.ask_str(text="text", validate="abc")


def test_str_valid(capsys, monkeypatch):
    """Test str validation."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = ["Xyz"]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            promptness.ask_str(text="text", validate="Xyz")


def test_str_empty_value_nodefault_emptyok(capsys, monkeypatch):
    """Test empty value returned when no value provided and emptyok=True."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = [""]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            v = promptness.ask_str(text="text", empty_ok=True)
            assert v == ""


def test_str_empty_value_default(capsys, monkeypatch):
    """Test default str value used when no value provided."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = [""]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            v = promptness.ask_str(text="text", default="Alpha")
            assert v == "Alpha"


def test_str_value(capsys, monkeypatch):
    """Test valid str value works."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = ["23"]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            v = promptness.ask_str(text="text")
            assert v == "23"


def test_str_value_default(capsys, monkeypatch):
    """Test valid str value with default works."""
    promptness = pytan3.utils.prompts.Promptness()
    inputs = ["23"]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            v = promptness.ask_str(text="text", default="Alpha")
            assert v == "23"


def test_dict_values_nodefault(capsys, monkeypatch):
    """Test ask dict with input values and no defaults."""
    promptness = pytan3.utils.prompts.Promptness()
    asks = [
        {"key": "num", "text": "Number", "method": "ask_int"},
        {"key": "name", "text": "Name", "method": "ask_str", "secure": False},
    ]
    inputs = ["23", "moo"]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            v = promptness.ask_dict(asks=asks)
    assert v == {"num": 23, "name": "moo"}


def test_dict_default_novalues(capsys, monkeypatch):
    """Test ask dict with no input values and defaults."""
    promptness = pytan3.utils.prompts.Promptness()
    asks = [
        {"key": "num", "text": "Number", "method": "ask_int", "default": 99},
        {
            "key": "name",
            "text": "Name",
            "method": "ask_str",
            "secure": False,
            "default": ".*",
        },
    ]
    inputs = ["", ""]
    with capsys.disabled():
        monkeypatch.setattr(promptness.input_stream, "isatty", isatty)
        monkeypatch.setattr(promptness.output_stream, "isatty", isatty)
        with input_mocker.InputMocker(inputs=inputs):
            v = promptness.ask_dict(asks=asks)
    assert v == {"num": 99, "name": ".*"}


def test_dict_overrides(capsys, monkeypatch):
    """Test ask dict with no input values and defaults with overrides."""
    promptness = pytan3.utils.prompts.Promptness()
    asks = [{"key": "num", "text": "Number", "method": "ask_int", "default": 99}]
    inputs = [""]
    over = {"num": 34}
    with capsys.disabled():
        with input_mocker.InputMocker(inputs=inputs):
            v = promptness.ask_dict(asks=asks, overrides=over)
    assert v == {"num": 34}

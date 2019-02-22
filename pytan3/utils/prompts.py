# -*- coding: utf-8 -*-
"""PyTan prompting module."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import colorama
import getpass
import logging
import os
import six
import sys
import re

colorama.init()


class ColorWrap(object):
    """Wrapper for colorama."""

    MODE_MAP = {"FORE": colorama.Fore, "BACK": colorama.Back, "STYLE": colorama.Style}
    """:obj:`dict`: Map of modes this wrapper can expose."""
    MODE = ""
    """:obj:`str`: Mode to wrap around colorama."""

    def __init__(self, mode=""):
        """Constructor.

        Args:
            mode (:obj:`str`, optional):
                One of keys in :attr:`MODE_MAP`.

                Defaults to: "".

        """
        self.MODE = mode
        """:obj:`str`: Mode to wrap around colorama."""

    def __getattr__(self, attr):
        """Get an attribute from colorama.

        Args:
            attr (:obj:`str`):
                If :attr:`MODE` is in `MODE_MAP`, get uppercased attr from MODE.

                Returns an empty string if MODE is not in MODE_MAP or attr is not
                available in MODE_CLS from MODE_MAP[MODE].

        Returns:
            :obj:`str`

        """
        mode = super(ColorWrap, self).__getattribute__("MODE")
        mode_map = super(ColorWrap, self).__getattribute__("MODE_MAP")
        mode_cls = mode_map.get(mode.upper(), None)
        attr = "RESET_ALL" if attr.upper() == "RESET" else attr.upper()
        color = getattr(mode_cls, attr, "")
        return color


class Promptness(object):
    """Prompt utility class."""

    YES_VALUES = ["y.*", "true", "1"]
    """:obj:`list` of :obj:`str`: Valid regex values for truthy-ness."""
    NO_VALUES = ["n.*", "false", "0"]
    """:obj:`list` of :obj:`str`: Valid regex values for falsey-ness."""
    USE_COLOR = True
    """:obj:`bool`: Use color in :meth:`prepare`."""
    OVERRIDES = None
    """:obj:`dict`: Default overrides for :meth:`Promptness.ask_dict`."""
    TMPLS = {
        "prompt": ("\n{{f.cyan}}{text}{{s.reset}} [default: {default}]: "),
        "value": "{{s.reset}}{{f.green}}'{value}'{{s.reset}}",
        "secure_value": "{{s.reset}}{{f.red}}..HIDDEN..{{s.reset}}",
        "env_value": (
            "\n{{f.green}}OS Environment Variable {env!r} has value {env_value}, "
            "{{f.green}}{action} override default {default}{{s.reset}}."
        ),
        "warn_notty": (
            "\n\n{{f.red}}No TTY on stream {stream}, using "
            "default {default!r} for {text!r}{{s.reset}}\n"
        ),
        "warn_option_invalid": (
            "\n-- {{f.red}}Value must be one of: {options!r}{{s.reset}}\n"
        ),
        "warn_nodefault": (
            "\n-- {{f.red}}No default defined, value required!{{s.reset}}"
        ),
        "warn_bool_invalid": (
            "\n-- {{f.red}}Value must be one of {yes_values!r} or {no_values!r}"
            "{{s.reset}}"
        ),
        "warn_int_invalid": ("\n-- {{f.red}}Value must be a valid number{{s.reset}}"),
        "warn_text_invalid": (
            "\n-- {{f.red}}Value did not match {validate!r}{{s.reset}}"
        ),
        "options": ("\nOptions:{options}\n"),
        "option": ("\n  {{f.BLUE}}{opt}{{s.reset}}"),
    }
    """:obj:`dict`: String templates used throughout."""

    def __init__(self, input_stream=sys.stdin, output_stream=sys.stderr, lvl="info"):
        """Constructor.

        Args:
            input_stream (:obj:`io.IOBase`, optional):
                Stream to get input from.

                Defaults to: :obj:`sys.stdin`.
            output_stream (:obj:`io.IOBase`, optional):
                Stream to send output to.

                Defaults to: :obj:`sys.stderr`.
            lvl (:obj:`str`, optional):
                Logging level for this object.

                Defaults to: "info".

        """
        self.input_stream = input_stream
        """:obj:`io.IOBase`: Stream to get input from."""
        self.output_stream = output_stream
        """:obj:`io.IOBase`: Stream to send output to."""
        self.log = logging.getLogger(__name__)
        """:obj:`logging.Logger`: Log for this object."""
        self.log.setLevel(getattr(logging, lvl.upper()))

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        bits = [
            "input={!r}".format(stream_name(self.input_stream)),
            "output={!r}".format(stream_name(self.output_stream)),
        ]
        bits = "({})".format(", ".join(bits))
        cls = "{c.__module__}.{c.__name__}".format(c=self.__class__)
        return "{cls}{bits}".format(cls=cls, bits=bits)

    def __repr__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        return self.__str__()

    def spew(self, text, **kwargs):
        """Print output to stream.

        Args:
            text (:obj:`str`):
                String to print.
            **kwargs:
                stream (:obj:`io.IOBase`):
                    Stream print to.

                    Defaults to: :attr:`output_stream`.

        """
        stream = kwargs.get("stream", self.output_stream)
        args = {"end": "", "file": stream}
        if six.PY3:
            args["flush"] = True
        print(text, **args)

    def prepare(self, text, **kwargs):
        """Format text with colors.

        Args:
            text (:obj:`str`):
                String to format.
            **kwargs:
                use_color (:obj:`bool`):
                    True: Replace fore, back, and style with color codes.

                    False: Replace fore, back, and style with empty vals.

                    Defaults to: :attr:`USE_COLOR`.

        """
        use_color = kwargs.get("use_color", self.USE_COLOR)
        fore = ColorWrap(mode="fore" if use_color else "")
        back = ColorWrap(mode="back" if use_color else "")
        style = ColorWrap(mode="style" if use_color else "")
        return text.format(f=fore, b=back, s=style)

    def get_prompter(self, secure=False):
        """Get a prompt function.

        Args:
            secure (:obj:`bool`, optional):
                Return getpass.getpass instead of input.

                Defaults to: False.

        Returns:
            :obj:`object`

        """
        return getpass.getpass if secure else six.moves.input

    def prompt(self, text, default=None, **kwargs):
        """Prompt for a value.

        Args:
            text (:obj:`str`):
                Prompt text from parent for error/warning messages.
            default (:obj:`object`, optional):
                Default value to use if no value supplied.

                Defaults to: None.
            **kwargs:
                secure (:obj:`bool`, optional):
                    If value should have its input hidden or not.

                    Defaults to: False.
                check_tty (:obj:`bool`):
                    Skip TTY checks for input/output stream.

                    Defaults to: False.
                env_var (:obj:`str`):
                    Replace default with contents of this OS Env.

                    Defaults to: "".
                rest of kwargs:
                    Passed to :meth:`spew` and :meth:`prepare`.

        Raises:
            :exc:`NoTtyError`:
                If the input or output stream is not attached to a console
                and check_tty is False.

        Returns:
            :obj:`str`

        """
        secure = kwargs.pop("secure", False)
        check_tty = kwargs.pop("check_tty", True)
        env_var = kwargs.pop("env_var", "")

        def_tmpl = "secure_value" if secure and default is not None else "value"
        def_tmpl = self.TMPLS[def_tmpl]
        def_text = def_tmpl.format(value="" if default is None else default)

        if env_var:
            env_val = os.environ.get(env_var, "")
            action = "will" if env_val else "will not"

            env_val_tmpl = "secure_value" if secure and env_val else "value"
            env_val_tmpl = self.TMPLS[env_val_tmpl]
            env_val_text = env_val_tmpl.format(value=env_val)

            prompt_env_tmpl = self.TMPLS["env_value"]
            prompt_env_text = prompt_env_tmpl.format(
                env=env_var, env_value=env_val_text, default=def_text, action=action
            )
            prompt_env_text = self.prepare(text=prompt_env_text, **kwargs)
            self.spew(text=prompt_env_text, **kwargs)
            default = env_val if env_val else default

        streams = [self.input_stream, self.output_stream]
        for stream in streams:
            if check_tty and not isatty(stream=stream):
                if default is None:
                    raise NoTtyError(stream=stream, text=text)
                w = self.TMPLS["warn_notty"].format(
                    stream=stream_name(stream), default=default, text=text
                )
                w = self.prepare(text=w, **kwargs)
                self.spew(text=w, **kwargs)
                return default

        prompt_tmpl = self.TMPLS["prompt"]
        prompt_text = prompt_tmpl.format(text=text, default=def_text)
        prompt_text = self.prepare(text=prompt_text, **kwargs)
        self.spew(text=prompt_text, **kwargs)

        v = self.get_prompter(secure=secure)("").strip()
        return format(default) if not v and default is not None else v

    def ask_choice(self, text, choices, default=None, attempts=5, **kwargs):
        """Prompt user to select from a list of choices.

        Args:
            text (:obj:`str`):
                Text to use when prompting.
            choices (:obj:`list` of :obj:`str`):
                List of choices for user to pick from.
            default (:obj:`str`, optional):
                Default value to use if no value supplied.

                Defaults to: None.
            attempts (:obj:`int`, optional):
                Number of attempts to allow empty/invalid input.

                Defaults to: 5.
            **kwargs:
                Passed to :meth`prepare` and :meth:`spew`.

        Raises:
            :exc:`InvalidValueError`:
                If value supplied is not one of choices.
            :exc:`EmptyValueError`:
                If no value supplied and no default.

        Returns:
            :obj:`str`

        """
        options = [format(x).lower() for x in choices]
        options_cr = "".join(self.TMPLS["option"].format(opt=x) for x in options)
        options_csv = ", ".join(options)

        pre_text = self.TMPLS["options"].format(options=options_cr)
        pre_text = self.prepare(text=pre_text, **kwargs)

        invalid_text = self.TMPLS["warn_option_invalid"].format(options=options_csv)
        invalid_text = self.prepare(text=invalid_text, **kwargs)

        nodefault_text = self.TMPLS["warn_nodefault"].format()
        nodefault_text = self.prepare(text=nodefault_text, **kwargs)

        invalid = False
        for i in range(attempts):
            self.spew(text=pre_text, **kwargs)
            value = self.prompt(text=text, default=default, **kwargs)
            if value:
                if value.lower() in options:
                    return choices[options.index(value.lower())]
                self.spew(text=invalid_text, **kwargs)
                invalid = True
            elif default is None:
                self.spew(text=nodefault_text, **kwargs)

        if invalid:
            raise InvalidValueError(text=text, attempts=attempts)
        else:
            raise EmptyValueError(text=text, attempts=attempts)

    def ask_bool(self, text, default=None, attempts=5, **kwargs):
        """Prompt user to provide yes or no.

        Args:
            text (:obj:`str`):
                Text to use when prompting.
            default (:obj:`bool` or :obj:`str`, optional):
                Default value to use if no value supplied.

                Defaults to: None.
            attempts (:obj:`int`, optional):
                Number of attempts to allow empty/invalid input.

                Defaults to: 5.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`prepare` and :meth:`spew`.

        Raises:
            :exc:`InvalidValueError`:
                If value supplied is not a valid yes/no string.
            :exc:`EmptyValueError`:
                If no value supplied and no default.

        Returns:
            :obj:`bool`

        """
        text += " (boolean)"

        invalid_text = self.TMPLS["warn_bool_invalid"].format(
            yes_values=", ".join(self.YES_VALUES), no_values=", ".join(self.NO_VALUES)
        )
        invalid_text = self.prepare(text=invalid_text, **kwargs)

        nodefault_text = self.TMPLS["warn_nodefault"].format()
        nodefault_text = self.prepare(text=nodefault_text, **kwargs)

        invalid = False
        for i in range(attempts):
            value = self.prompt(text=text, default=default, **kwargs)
            if value:
                if any(re.match(p, value, re.IGNORECASE) for p in self.YES_VALUES):
                    return True
                if any(re.match(p, value, re.IGNORECASE) for p in self.NO_VALUES):
                    return False
                self.spew(text=invalid_text, **kwargs)
                invalid = True
            elif default is None:
                self.spew(text=nodefault_text, **kwargs)

        if invalid:
            raise InvalidValueError(text=text, attempts=attempts)
        else:
            raise EmptyValueError(text=text, attempts=attempts)

    def ask_int(self, text, default=None, attempts=5, **kwargs):
        """Prompt user to provide yes or no.

        Args:
            text (:obj:`str`):
                Text to use when prompting.
            default (:obj:`int`, optional):
                Default value to use if no value supplied.

                Defaults to: None.
            attempts (:obj:`int`, optional):
                Number of attempts to allow empty/invalid input.

                Defaults to: 5.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`prompt` and :meth:`prepare`.

        Raises:
            :exc:`InvalidValueError`:
                If value supplied is not an int.
            :exc:`EmptyValueError`:
                If no value supplied and no default.

        Returns:
            :obj:`int`

        """
        text += " (integer)"

        invalid_text = self.TMPLS["warn_int_invalid"].format()
        invalid_text = self.prepare(text=invalid_text, **kwargs)

        nodefault_text = self.TMPLS["warn_nodefault"].format()
        nodefault_text = self.prepare(text=nodefault_text, **kwargs)

        invalid = False
        for i in range(attempts):
            value = self.prompt(text=text, default=default, **kwargs)
            if value:
                if format(value).isdigit():
                    return int(value)
                self.spew(text=invalid_text, **kwargs)
                invalid = True
            elif default is None:
                self.spew(text=nodefault_text, **kwargs)

        if invalid:
            raise InvalidValueError(text=text, attempts=attempts)
        else:
            raise EmptyValueError(text=text, attempts=attempts)

    def ask_str(self, text, default=None, attempts=5, **kwargs):
        """Prompt user to provide yes or no.

        Args:
            text (:obj:`str`):
                Text to use when prompting.
            default (:obj:`str`, optional):
                Default value to use if no value supplied.

                Defaults to: "".
            attempts (:obj:`int`, optional):
                Number of attempts to allow empty/invalid input.

                Defaults to: 5.
            **kwargs:
                empty_ok (:obj:`bool`, optional):
                    Empty input is allowed.

                    Defaults to: False.
                validate (:obj:`str`, optional):
                    Regex string to validate value.

                    Defaults to: "".
                rest of kwargs:
                    Passed to :meth:`prompt` and :meth:`prepare`.

        Raises:
            :exc:`EmptyValueError`:
                If no value supplied and no default and not empty_ok.

        Returns:
            :obj:`str`

        """
        empty_ok = kwargs.pop("empty_ok", False)
        validate = kwargs.pop("validate", "")

        text += " (string)"
        invalid_text = self.TMPLS["warn_text_invalid"].format(validate=validate)
        invalid_text = self.prepare(text=invalid_text, **kwargs)

        nodefault_text = self.TMPLS["warn_nodefault"].format()
        nodefault_text = self.prepare(text=nodefault_text, **kwargs)

        invalid = False
        for i in range(attempts):
            value = self.prompt(text=text, default=default, **kwargs)
            if value:
                if validate:
                    match = re.search(validate, value, re.IGNORECASE)
                    if match:
                        return value
                    self.spew(text=invalid_text, **kwargs)
                    invalid = True
                else:
                    return value
            elif empty_ok:
                return value
            elif default is None:
                self.spew(text=nodefault_text, **kwargs)
                continue

        if invalid:
            raise InvalidValueError(text=text, attempts=attempts)
        else:
            raise EmptyValueError(text=text, attempts=attempts)

    # LATER(!) automagic ask method for method
    def ask_dict(self, asks, overrides=None):
        """Prompt for input from a list of dict.

        Args:
            asks (:obj:`list` of :obj:`dict`):
                List of dicts with valid kwargs for the various ask methods.
            overrides: (:obj:`dict`, optional):
                Dictionary of key / value pairs to over ride the defaults of asks.

                Defaults to: None.

        Notes:
            Keys for ask dict in asks:

            "method", required:
                Ask method to use for this ask dict.
            "key", required:
                Key to store value returned from ask method in return dict.
            "text", required:
                String to use for prompting.
            "choices", required for :meth:`ask_choice`:
                List of valid choices for user to pick.
            "secure", optional for :meth:`ask_str`:
                Use prompt that hides user input while typing.
            "default", optional:
                Default value to use if user does not provide one.
            "attempts", optional:
                Number of attempts to allow empty/invalid input.
            "check_tty", optional:
                Skip TTY checks for input/output stream.

        Returns:
            :obj:`dict`

        """
        over = {}
        over.update(self.OVERRIDES or {})
        over.update(overrides or {})
        values = {}
        # need_keys = ["key", "method", "text"]
        for ask in asks:
            # if not any(key in ask for key in need_keys):
            #     error = "Must provide keys {keys!r} in {ask!r}"
            #     error = error.format(keys=need_keys, ask=ask)
            #     raise PromptError(text=error, attempts=0)
            default = ask.get("default", None)
            ask["default"] = over.get(ask["key"], default)
            values[ask["key"]] = getattr(self, ask["method"])(**ask)
        return values


class PromptError(Exception):
    """Parent exception for any errors when prompting.

    Thrown by:
        :meth:`Promptness.ask_dict`

    """

    msg = "{text}"

    def __init__(self, text, attempts):
        """Constructor.

        Args:
            text (:obj:`str`):
                Text to insert into exception message
            attempts (:obj:`int`, optional):
                Number of attempts tried before this exception
        """
        msg = self.msg.format(text=text, attempts=attempts)
        super(PromptError, self).__init__(msg)


class InvalidValueError(PromptError):
    """Thrown when a user provides an invalid value.

    Thrown by:
        :meth:`Promptness.ask_choice`
        :meth:`Promptness.ask_bool`
        :meth:`Promptness.ask_int`

    """

    msg = "Invalid value supplied for prompt {text!r} after {attempts} attempts"


class EmptyValueError(PromptError):
    """Thrown when no default defined and user provides no value.

    Thrown by:
        :meth:`Promptness.ask_choice`
        :meth:`Promptness.ask_bool`
        :meth:`Promptness.ask_int`
        :meth:`Promptness.ask_str`

    """

    msg = "No value supplied for prompt {text!r} after {attempts} attempts"


class NoTtyError(PromptError):
    """Thrown when a TTY is not attached to a console.

    Thrown by:
        :meth:`Promptness.prompt`

    """

    def __init__(self, stream, text):
        """Constructor.

        Args:
            stream (:obj:`io.IOBase`):
                Stream that was not attached to a console.
            text (:obj:`str`):
                Text to insert into exception message

        """
        stmpl = "{stream}, {name}, {istty}".format
        streams = [sys.stdin, sys.stdout, sys.stderr]
        streams = [
            stmpl(stream=s, name=stream_name(s), istty=isatty(s)) for s in streams
        ]

        msg = "\n".join(
            [
                "No TTY on stream {s} and no default value for {text!r}, all streams:",
                "  " + "\n  ".join(streams),
            ]
        )
        msg = msg.format(s=stream_name(stream), text=text)

        super(PromptError, self).__init__(msg)


def stream_name(stream):
    """Get the name of a stream.

    Args:
        stream (:obj:`io.IOBase`):
            Stream to get name of.

    Returns:
        :obj:`str`

    """
    try:
        return stream.name
    except Exception:
        return stream.__class__.__name__


def isatty(stream):
    """Check if a stream is attached to a console.

    Args:
        stream (:obj:`io.IOBase`):
            Stream to check.

    Returns:
        :obj:`bool`

    """
    return stream.isatty() if hasattr(stream, "isatty") else False


promptness = Promptness()
""":obj:`Promptness`: Pre-established object for easy usage."""

# -*- coding: utf-8 -*-
"""Exceptions and warnings for :mod:`pytan3.auth_methods`."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions


class ModuleError(exceptions.PyTanError):
    """Parent of all exceptions for :mod:`pytan3.auth_methods`.

    Thrown by:
      * :func:`pytan3.auth_methods.load`

    """

    pass


class ModuleWarning(exceptions.PyTanWarning):
    """Parent of all warnings for :mod:`pytan3.auth_methods`.

    Thrown by:

    """

    pass


class MethodError(ModuleError):
    """Parent of all :obj:`pytan3.auth_methods.AuthMethod` exceptions.

    Thrown by:

    """

    msg = "Authentication Method Error!"
    """:obj:`str`: Error message to use in exception."""

    def __init__(self, auth_method, info=None, response=None):
        """Constructor.

        Args:
            auth_method (:obj:`pytan3.auth_methods.AuthMethod`):
                Object where exception was thrown from.
            info (:obj:`str`, optional):
                Additional error info message to show.

                Defaults to: None.
            response (:obj:`requests.Response`, optional):
                Response associated with this exception, if any.

                Defaults to: None.
        """
        self.auth_method = auth_method
        self.response = response

        msgs = ["AuthMethod: {a}".format(a=auth_method)]

        if response is not None:
            msgs += [
                "Response body: {r}".format(r=response.clean_body),
                "Request URL: {r!r}".format(r=response.url),
                "Request method: {r!r}".format(r=response.request.method),
                "Response status code: {r!r}".format(r=response.status_code),
            ]

        msgs.append("Error: {m}".format(m=self.msg))
        error = "\n\t" + "\n\t".join(msgs)
        self.error = error
        """:obj:`str`: Error message that was thrown."""
        super(MethodError, self).__init__(error)


class InvalidToken(MethodError):
    """Thrown when validate_token fails.

    Thrown by:
        * :meth:`pytan3.auth_methods.AuthMethod.validate`

    """

    msg = "Supplied token is invalid!"
    """:obj:`str`: Error message to use in exception."""


class NotLoggedInError(MethodError):
    """Thrown when logout called before login.

    Thrown by:
        * :meth:`pytan3.auth_methods.AuthMethod.validate`
        * :meth:`pytan3.auth_methods.AuthMethod.logout`
        * :meth:`pytan3.auth_methods.AuthMethod.logout_all`

    """

    msg = "Not logged in, unable to logout/validate token. Must login first!"
    """:obj:`str`: Error message to use in exception."""


class LoginError(MethodError):
    """Thrown when login response has any status_code other than 200.

    Thrown by:
        * :meth:`pytan3.auth_methods.AuthMethod.login`

    """

    msg = "Login failed. Response status code is not 200!"
    """:obj:`str`: Error message to use in exception."""


class LogoutError(MethodError):
    """Thrown when logout fails.

    Thrown by:
        * :meth:`pytan3.auth_methods.AuthMethod.logout`
        * :meth:`pytan3.auth_methods.AuthMethod.logout_all`

    """

    msg = "Logout failed. Verify the supplied credentials!"
    """:obj:`str`: Error message to use in exception."""

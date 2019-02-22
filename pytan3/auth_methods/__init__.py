# -*- coding: utf-8 -*-
"""Authentication methods for the Tanium API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import abc
import datetime
import json
import six
import re

from . import exceptions
from .. import utils
from .. import api_clients
from .. import auth_store

DEFAULT_NAME = "credentials"
""":obj:`str`: Default :class:`AuthMethod` name to load in :func:`load`."""


@six.add_metaclass(abc.ABCMeta)
class AuthMethod(object):
    """Abstract base class for all AuthMethods."""

    @classmethod
    @abc.abstractmethod
    def get_name(cls):
        """Get the ref name of this class for use by :func:`load`.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @classmethod
    @abc.abstractmethod
    def get_version_req(cls):
        """Get the min, max, and eq version requirements of this class.

        Notes:
            Dict can specify keys: "vmin", "vmax", "veq".

            This class method gets called by
            :func:`pytan3.utils.versions.version_check_obj_req` to perform version
            checks.

        Returns:
            :obj:`dict`

        """
        raise NotImplementedError  # pragma: no cover

    @classmethod
    @abc.abstractmethod
    def get_args(cls):
        """Get all arguments used by this class.

        Returns:
            :obj:`list`

        """
        raise NotImplementedError  # pragma: no cover

    @classmethod
    @abc.abstractmethod
    def get_args_required(cls):
        """Get all arguments used by this class that are required.

        Returns:
            :obj:`list`

        """
        raise NotImplementedError  # pragma: no cover

    @classmethod
    @abc.abstractmethod
    def get_args_secure(cls):
        """Get all arguments used by this class that need their prompt input hidden.

        Returns:
            :obj:`list`

        """
        raise NotImplementedError  # pragma: no cover

    @classmethod
    @abc.abstractmethod
    def from_store(cls, store, **kwargs):
        """Create an instance of this class from an :obj:`pytan3.auth_store.AuthStore`.

        Args:
            store (:obj:`pytan3.auth_store.AuthStore`):
                AuthStore to get AuthMethod arguments from.

        Returns:
            :obj:`AuthMethod`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def http_client(self):
        """Get the HTTP Client for this object.

        Returns:
            :obj:`pytan3.http_client.HttpClient`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def token(self):
        """Get or set a token.

        Notes:
            If no token received, :meth:`login` to get one.

            If token expired, :meth:`login` to get a new one.

            If token has been received, :meth:`validate` to validate token.

            If token fails validation, :meth:`login` to get a new one.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def token_headers(self):
        """Get dict with :attr:`token` for use in headers.

        Returns:
            :obj:`dict`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def uid(self):
        """Get user ID for token if a token has been received.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def logged_in(self):
        """Check if a token has been received.

        Returns:
            :obj:`bool`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def login(self, **kwargs):
        """Send a login request to receive a token.

        Raises:
            :exc:`exceptions.LoginError`:
                If status code in response is not 200.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def logout(self, **kwargs):
        """Send a logout request to revoke a token.

        Raises:
            :exc:`exceptions.NotLoggedInError`:
                If :attr:`logged_in` is False.
            :exc:`exceptions.LogoutError`:
                If status code in response is not 200.

        Returns:
            None

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def logout_all(self, **kwargs):
        """Send a logout request to revoke all tokens associated with this token.

        Raises:
            :exc:`exceptions.NotLoggedInError`:
                If :attr:`logged_in` is False.
            :exc:`exceptions.LogoutError`:
                If status code in response is not 200.

        Returns:
            None

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def validate(self, **kwargs):
        """Send a validate request to check that token is still valid.

        Raises:
            :exc:`exceptions.NotLoggedInError`:
                If :attr:`logged_in` is False.
            :exc:`exceptions.InvalidToken`:
                If status code in response is not 200.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def create_store(self, **kwargs):
        """Create an instance of :obj:`pytan3.auth_store.AuthStore` from this object.

        Returns:
            :obj:`pytan3.auth_store.AuthStore`

        """
        raise NotImplementedError  # pragma: no cover


class CommonMixin(object):
    """Shared methods common amongst all :class:`AuthMethod`."""

    def __init__(
        self,
        http_client,
        login_timeout=5,
        logout_timeout=5,
        expires_after=295,
        ver_check=True,
        lvl="info",
    ):
        """Constructor.

        Args:
            http_client (:obj:`pytan3.http_client.HttpClient`):
                Object for sending HTTP requests.
            login_timeout (:obj:`int`, optional):
                Timeout for login and validate responses in seconds.

                Defaults to: 5.
            logout_timeout (:obj:`int`, optional):
                Timeout for logout responses in seconds.

                Defaults to: 5.
            expires_after (:obj:`int`, optional):
                Life of received tokens in seconds.

                Defaults to: 295.
            ver_check (:obj:`bool`, optional):
                Perform version checks against the platform version from
                :func:`pytan3.api_clients.get_version` using
                :func:`pytan3.utils.versions.version_check_obj_req`.

                Defaults to: True.
            lvl (:obj:`str`, optional):
                Logging level for this object.

                Defaults to: "info".

        """
        self.log = utils.logs.get_obj_log(obj=self, lvl=lvl)
        """:obj:`logging.Logger`: Log for this object."""

        self.revalidate_after = 5
        """:obj:`int`: Revalidate token if :attr:`last_used` is higher than this."""

        self._http_client = http_client
        self._login_timeout = login_timeout
        self._logout_timeout = logout_timeout
        self._expires_after = expires_after
        self._last_used = None
        self._token = None
        self.token = None
        if ver_check and any(self.get_version_req().values()):
            utils.versions.version_check_obj_req(
                version=api_clients.get_version(self.http_client),
                src=self.http_client.url,
                obj=self,
            )

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        last_used = utils.tools.human_delta(self._last_used) or "NEVER"
        expires_in = self._expires_after - (self.last_used or 0)
        expires_in = "EXPIRED" if self.expired else utils.tools.human_delta(expires_in)
        bits = [
            "logged_in={!r}".format(self.logged_in),
            "last_used={!r}".format(last_used),
            "expires_in={!r}".format(expires_in),
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

    @classmethod
    def from_store(cls, store, **kwargs):
        """Create an instance of this class from an :obj:`pytan3.auth_store.AuthStore`.

        Args:
            store (:obj:`pytan3.auth_store.AuthStore`):
                AuthStore to get AuthMethod arguments from.
            **kwargs:
                Rest of kwargs passed to :class:`AuthMethod`.

        Returns:
            :obj:`AuthMethod`

        """
        method_cls = load(store.method)
        args = method_cls.get_args()
        req_args = method_cls.get_args_required()
        kwargs.setdefault("http_client", store.http_client)
        kwargs.update({k: store.get(k, required=k in req_args) for k in args})
        return method_cls(**kwargs)

    @property
    def http_client(self):
        """Get the HTTP Client for this object.

        Returns:
            :obj:`pytan3.http_client.HttpClient`

        """
        return self._http_client

    @property
    def token(self):
        """Get a token.

        Notes:
            If :attr:`logged_in` is False, :meth:`login` to get one.

            If :attr:`expired` is True, :meth:`login` to get a new one.

            If :attr:`logged_in` is True, and :attr:`last_used` is older than
            :attr:`revalidate_after`, :meth:`validate` to re-validate token.

            If :meth:`validate` fails validation, :meth:`login` to get a new one.

        Returns:
            :obj:`str`

        """
        if not self.logged_in:
            self.login(cause="Initial login")
        elif self.expired:
            self.login(cause="Re-login due to expired token")
        else:
            if self.last_used is None or self.last_used >= self.revalidate_after:
                try:
                    self.validate(cause="Validate existing token")
                except exceptions.InvalidToken:
                    m = "Token for User ID {uid!r} no longer valid, getting new one"
                    m = m.format(uid=self.uid)
                    self.log.debug(m)
                    self.login(cause="Re-login due to invalid token")
        return self._token

    @token.setter
    def token(self, value):
        """Set the token to value and :attr:`last_used` to now.

        Args:
            value (:obj:`str`):
                Value to set _token to

        """
        self._token = value
        if value is None:
            self._last_used = None
        else:
            self._last_used = datetime.datetime.utcnow()

    @property
    def token_headers(self):
        """Get dict with :attr:`token` for use in headers.

        Returns:
            :obj:`dict`

        """
        return {"session": self.token}

    @property
    def uid(self):
        """Get user ID for token if a token has been received.

        Returns:
            :obj:`str`

        """
        return int((self._token or self.token).split("-")[0])

    @property
    def logged_in(self):
        """Check if a token has been received.

        Returns:
            :obj:`bool`

        """
        return True if self._token else False

    @property
    def expired(self):
        """Check if token has expired.

        Returns:
            :obj:`bool`

        """
        return self.last_used is None or self.last_used >= self._expires_after

    @property
    def last_used(self):
        """Get the number of seconds since token was issued or last used.

        Returns:
            :obj:`int`

        """
        # is_none = self._last_used is None
        return (
            None if self._last_used is None else utils.tools.secs_age(self._last_used)
        )

    def login(self, **kwargs):
        """Send a login request to receive a token.

        Args:
            **kwargs:
                cause (:obj:`str`):
                    String to explain purpose of request.

                    Defaults to: "Get new token".

        Raises:
            :exc:`exceptions.LoginError`:
                If status code in response is not 200.

        Returns:
            :obj:`str`

        """
        r = self.http_client(
            path="/auth",
            method="post",
            headers={k: v for k, v in self._headers.items() if v},
            b64_headers=self._b64_headers,
            timeout=self._login_timeout,
            cause=kwargs.pop("cause", "Get new token"),
        )

        if r.status_code != 200:
            raise exceptions.LoginError(auth_method=self, response=r)

        self.token = r.text
        m = "Token received for User ID {uid!r} from {url!r}"
        m = m.format(uid=self.uid, url=r.url)
        self.log.debug(m)
        return r.text

    def logout(self, **kwargs):
        """Send a logout request to revoke a token.

        Args:
            **kwargs:
                cause (:obj:`str`):
                    String to explain purpose of request.

                    Defaults to: "Revoke token".
                headers (:obj:`dict`):
                    Headers to send in request.

                    Defaults to: {}.

        Raises:
            :exc:`exceptions.NotLoggedInError`:
                If :attr:`logged_in` is False.
            :exc:`exceptions.LogoutError`:
                If status code in response is not 200.

        Returns:
            None

        """
        if not self.logged_in:
            raise exceptions.NotLoggedInError(auth_method=self)

        r = self.http_client(
            path="/auth",
            method="post",
            headers={"session": self._token, "logout": "0"},
            b64_headers=self._b64_headers,
            timeout=self._logout_timeout,
            cause=kwargs.pop("cause", "Revoke token"),
        )

        if r.status_code != 200:
            raise exceptions.LogoutError(auth_method=self, response=r)

        m = "Token revoked for User ID {uid!r} from {url!r}"
        m = m.format(uid=self.uid, url=r.url)
        self.log.debug(m)
        self.token = None
        return None

    def logout_all(self, **kwargs):
        """Send a logout request to revoke all tokens associated with this token.

        Args:
            **kwargs:
                cause (:obj:`str`):
                    String to explain purpose of request.

                    Defaults to: "Revoke all tokens".
                headers (:obj:`dict`):
                    Headers to send in request.

                    Defaults to: {}.

        Raises:
            :exc:`exceptions.NotLoggedInError`:
                If :attr:`logged_in` is False.
            :exc:`exceptions.LogoutError`:
                If status code in response is not 200.

        Returns:
            None

        """
        if not self.logged_in:
            raise exceptions.NotLoggedInError(auth_method=self)

        r = self.http_client(
            path="/auth",
            method="post",
            headers={"session": self._token, "logout": "1"},
            b64_headers=self._b64_headers,
            timeout=self._logout_timeout,
            cause=kwargs.pop("cause", "Revoke all tokens"),
        )

        if r.status_code != 200:
            raise exceptions.LogoutError(auth_method=self, response=r)

        m = "All tokens revoked for User ID {uid!r} from {url!r}"
        m = m.format(uid=self.uid, url=r.url)
        self.log.debug(m)
        self.token = None
        return None

    def validate(self, **kwargs):
        """Send a validate request to check that token is still valid.

        Args:
            **kwargs:
                cause (:obj:`str`):
                    String to explain purpose of request.

                    Defaults to: "Validate token".
                headers (:obj:`dict`):
                    Headers to send in request.

                    Defaults to: {}.

        Raises:
            :exc:`exceptions.NotLoggedInError`:
                If :attr:`logged_in` is False.
            :exc:`exceptions.InvalidToken`:
                If status code in response is not 200.

        Returns:
            :obj:`str`

        """
        if not self.logged_in:
            raise exceptions.NotLoggedInError(auth_method=self)

        r = self.http_client(
            path="/auth",
            method="post",
            headers={"session": self._token},
            timeout=self._login_timeout,
            cause=kwargs.pop("cause", "Validate token"),
        )

        if r.status_code != 200:
            raise exceptions.InvalidToken(auth_method=self, response=r)

        m = "Token validated for User ID {uid!r} from {url!r}"
        m = m.format(uid=self.uid, url=r.url)
        self.log.debug(m)
        self.token = r.text
        return r.text

    def create_store(self, **kwargs):
        """Create an instance of :obj:`pytan3.auth_store.AuthStore` from this object.

        Returns:
            :obj:`pytan3.auth_store.AuthStore`

        """
        kwargs.setdefault("http_client", self.http_client)
        kwargs.setdefault("src", "method")
        store = auth_store.AuthStore(**kwargs)
        store.method = self
        for key in self.get_args():
            store.set(key=key, value=self._headers[key])
        return store


class Credentials(CommonMixin, AuthMethod):
    """Method that uses credentials to interact with the '/auth' API."""

    def __init__(
        self,
        http_client,
        username,
        password,
        domain="",
        secondary="",
        login_timeout=5,
        logout_timeout=5,
        expires_after=295,
        ver_check=True,
        lvl="info",
    ):
        """Constructor.

        Args:
            http_client (:obj:`pytan3.http_client.HttpClient`):
                HTTP client.
            username (:obj:`str`):
                Header to pass to /auth API.
            password (:obj:`str`):
                Header to pass to /auth API.
            domain (:obj:`str`, optional):
                Header to pass to /auth API.

                Defaults to: ""
            secondary (:obj:`str`, optional):
                Header to pass to /auth API.

                Defaults to: ""
            login_timeout (:obj:`int`, optional):
                Timeout for login and validate responses in seconds.

                Defaults to: 5.
            logout_timeout (:obj:`int`, optional):
                Timeout for logout responses in seconds.

                Defaults to: 5.
            expires_after (:obj:`int`, optional):
                Life of received tokens in seconds.

                Defaults to: 295.
            ver_check (:obj:`bool`, optional):
                Perform version checks against the platform version from
                :func:`pytan3.api_clients.get_version` using
                :func:`pytan3.utils.versions.version_check_obj_req`.

                Defaults to: True.
            lvl (:obj:`str`, optional):
                Logging level for this object.

                Defaults to: "info".

        """
        self._headers = {
            "username": username,
            "password": password,
            "domain": domain,
            "secondary": secondary,
        }
        self._b64_headers = ["username", "password"]
        super(Credentials, self).__init__(
            http_client=http_client,
            login_timeout=login_timeout,
            logout_timeout=logout_timeout,
            expires_after=expires_after,
            ver_check=ver_check,
            lvl=lvl,
        )

    @classmethod
    def get_name(cls):
        """Get the ref name of this class for use by :func:`load`.

        Returns:
            :obj:`str`

        """
        return "credentials"

    @classmethod
    def get_version_req(cls):
        """Get the min, max, and eq version requirements of this class.

        Notes:
            Dict can specify keys: "vmin", "vmax", "veq".

            This class method gets called by
            :func:`pytan3.utils.versions.version_check_obj_req` to perform version
            checks.

        Returns:
            :obj:`dict`

        """
        return {"vmin": "", "vmax": "", "veq": ""}

    @classmethod
    def get_args(cls):
        """Get all arguments used by this class.

        Returns:
            :obj:`list`

        """
        return ["username", "password", "secondary", "domain"]

    @classmethod
    def get_args_required(cls):
        """Get all arguments used by this class that are required.

        Returns:
            :obj:`list`

        """
        return ["username", "password"]

    @classmethod
    def get_args_secure(cls):
        """Get all arguments used by this class that need their prompt input hidden.

        Returns:
            :obj:`list`

        """
        return ["password"]


class SessionId(CommonMixin, AuthMethod):
    """Method that uses session id to interact with the '/auth' API."""

    def __init__(
        self,
        http_client,
        session,
        login_timeout=5,
        logout_timeout=5,
        expires_after=295,
        ver_check=True,
        lvl="info",
    ):
        """Constructor.

        Args:
            http_client (:obj:`pytan3.http_client.HttpClient`):
                HTTP client.
            session (:obj:`str`):
                Header to pass to /auth API.
            login_timeout (:obj:`int`, optional):
                Timeout for login and validate responses in seconds.

                Defaults to: 5.
            logout_timeout (:obj:`int`, optional):
                Timeout for logout responses in seconds.

                Defaults to: 5.
            expires_after (:obj:`int`, optional):
                Life of received tokens in seconds.

                Defaults to: 295.
            ver_check (:obj:`bool`, optional):
                Perform version checks against the platform version from
                :func:`pytan3.api_clients.get_version` using
                :func:`pytan3.utils.versions.version_check_obj_req`.

                Defaults to: True.
            lvl (:obj:`str`, optional):
                Logging level for this object.

                Defaults to: "info".

        """
        self._headers = {"session": session}
        self._b64_headers = []
        super(SessionId, self).__init__(
            http_client=http_client,
            login_timeout=login_timeout,
            logout_timeout=logout_timeout,
            expires_after=expires_after,
            ver_check=ver_check,
            lvl=lvl,
        )
        self.token = session

    @classmethod
    def get_name(cls):
        """Get the ref name of this class for use by :func:`load`.

        Returns:
            :obj:`str`

        """
        name = "session_id"
        return name

    @classmethod
    def get_version_req(cls):
        """Get the min, max, and eq version requirements of this class.

        Notes:
            Dict can specify keys: "vmin", "vmax", "veq".

            This class method gets called by
            :func:`pytan3.utils.versions.version_check_obj_req` to perform version
            checks.

        Returns:
            :obj:`dict`

        """
        return {"vmin": "", "vmax": "", "veq": ""}

    @classmethod
    def get_args(cls):
        """Get all arguments used by this class.

        Returns:
            :obj:`list`

        """
        return ["session"]

    @classmethod
    def get_args_required(cls):
        """Get all arguments used by this class that are required.

        Returns:
            :obj:`list`

        """
        return ["session"]

    @classmethod
    def get_args_secure(cls):
        """Get all arguments used by this class that need their prompt input hidden.

        Returns:
            :obj:`list`

        """
        return []

    @property
    def token(self):
        """Get a token.

        Notes:
            If :attr:`CommonMixin.logged_in` is False, can not login to get a
            new one with just a session.

            If :attr:`CommonMixin.expired` is True, can not login to get
            a new one with just a session.

            If :attr:`CommonMixin.logged_in` is True, and :attr:`CommonMixin.last_used`
            is older than :attr:`CommonMixin.revalidate_after`,
            :meth:`CommonMixin.validate` to re-validate token.

            If :meth:`CommonMixin.validate` fails validation, can not login
            to get a new one with just a session.

        Returns:
            :obj:`str`

        """
        if self.last_used is None or self.last_used >= self.revalidate_after:
            self.validate(cause="Validate existing token")
        return self._token

    @token.setter
    def token(self, value):
        """Set the token to value and :attr:`CommonMixin.last_used` to now.

        Args:
            value (:obj:`str`):
                Value to set _token to

        """
        self._token = value
        if value is None:
            self._last_used = None
            self._last_validated = None
        else:
            self._last_used = datetime.datetime.utcnow()
            self._last_validated = datetime.datetime.utcnow()

    def login(self, **kwargs):
        """Send a login request to receive a token.

        Raises:
            :exc:`exceptions.LoginError`:
                If status code in response is not 200.

        Returns:
            :obj:`str`

        """
        error = "Unable to perform a login with a session ID, can only validate"
        raise NotImplementedError(error)


class RestCredentials(CommonMixin, AuthMethod):
    """Method that uses credentials to interact with the REST 'session' API."""

    def __init__(
        self,
        http_client,
        username,
        password,
        domain="",
        secondary="",
        login_timeout=5,
        logout_timeout=5,
        expires_after=295,
        ver_check=True,
        lvl="info",
    ):
        """Constructor.

        Args:
            http_client (:obj:`pytan3.http_client.HttpClient`):
                HTTP client.
            username (:obj:`str`):
                Header to pass to /api/v2/session REST API.
            password (:obj:`str`):
                Header to pass to /api/v2/session REST API.
            domain (:obj:`str`, optional):
                Header to pass to /api/v2/session REST API.

                Defaults to: ""
            secondary (:obj:`str`, optional):
                Header to pass to /api/v2/session REST API.

                Defaults to: ""
            login_timeout (:obj:`int`, optional):
                Timeout for login and validate responses in seconds.

                Defaults to: 5.
            logout_timeout (:obj:`int`, optional):
                Timeout for logout responses in seconds.

                Defaults to: 5.
            expires_after (:obj:`int`, optional):
                Life of received tokens in seconds.

                Defaults to: 295.
            ver_check (:obj:`bool`, optional):
                Perform version checks against the platform version from
                :func:`pytan3.api_clients.get_version` using
                :func:`pytan3.utils.versions.version_check_obj_req`.

                Defaults to: True.
            lvl (:obj:`str`, optional):
                Logging level.

                Defaults to: "info".

        """
        self._headers = {
            "username": username,
            "password": password,
            "domain": domain,
            "secondary": secondary,
        }
        self._b64_headers = ["username", "password"]
        super(RestCredentials, self).__init__(
            http_client=http_client,
            login_timeout=login_timeout,
            logout_timeout=logout_timeout,
            expires_after=expires_after,
            ver_check=ver_check,
            lvl=lvl,
        )

    @classmethod
    def get_name(cls):
        """Get the ref name of this class for use by :func:`load`.

        Returns:
            :obj:`str`

        """
        return "rest_credentials"

    @classmethod
    def get_version_req(cls):
        """Get the min, max, and eq version requirements of this class.

        Notes:
            Dict can specify keys: "vmin", "vmax", "veq".

            This class method gets called by
            :func:`pytan3.utils.versions.version_check_obj_req` to perform version
            checks.

        Returns:
            :obj:`dict`

        """
        return {"vmin": "7.3.314.3409", "vmax": "", "veq": ""}

    @classmethod
    def get_args(cls):
        """Get all arguments used by this class.

        Returns:
            :obj:`list`

        """
        return ["username", "password", "secondary", "domain"]

    @classmethod
    def get_args_required(cls):
        """Get all arguments used by this class that are required.

        Returns:
            :obj:`list`

        """
        return ["username", "password"]

    @classmethod
    def get_args_secure(cls):
        """Get all arguments used by this class that need their prompt input hidden.

        Returns:
            :obj:`list`

        """
        return ["password"]

    @property
    def rest_version(self):
        """Version of REST API for this method.

        Returns:
            :obj:`int`

        """
        return 2

    def login(self, **kwargs):
        """Send a login request to receive a token.

        Args:
            **kwargs:
                cause (:obj:`str`): String to explain purpose of request.

                Defaults to: "Get new token".

        Raises:
            :exc:`exceptions.LoginError`:
                If status code in response is not 200.

        Returns:
            :obj:`str`

        """
        r = self.http_client(
            path="/api/v{v}/{e}".format(v=self.rest_version, e="session/login"),
            method="post",
            data=json.dumps({k: v for k, v in self._headers.items() if v}, indent=2),
            timeout=self._login_timeout,
            cause=kwargs.pop("cause", "Get new token"),
        )

        if r.status_code != 200:
            raise exceptions.LoginError(auth_method=self, response=r)

        token = r.json()["data"]["session"]
        self.token = token
        m = "Token received for User ID {uid!r} from {url!r}"
        m = m.format(uid=self.uid, url=r.url)
        self.log.debug(m)
        return token

    def logout(self, **kwargs):
        """Send a logout request to revoke a token.

        Args:
            **kwargs:
                cause (:obj:`str`): String to explain purpose of request.

                Defaults to: "Revoke token".

        Raises:
            :exc:`exceptions.NotLoggedInError`:
                If :attr:`CommonMixin.logged_in` is False.
            :exc:`exceptions.LogoutError`:
                If status code in response is not 200.

        Returns:
            None

        """
        if not self.logged_in:
            raise exceptions.NotLoggedInError(auth_method=self)

        r = self.http_client(
            path="/api/v{v}/{e}".format(v=self.rest_version, e="session/logout"),
            method="post",
            data=json.dumps({"session": self._token}),
            timeout=self._login_timeout,
            cause=kwargs.pop("cause", "Revoke token"),
        )

        if r.status_code != 200:
            raise exceptions.LogoutError(auth_method=self, response=r)

        m = "Token revoked for User ID {uid!r} from {url!r}"
        m = m.format(uid=self.uid, url=r.url)
        self.log.debug(m)
        self.token = None
        return None

    def logout_all(self, **kwargs):
        """Send a logout request to revoke all tokens associated with this token.

        Raises:
            :exc:`NotImplementedError`:
                REST 'session' endpoint does not have a logout all target.

        """
        error = "REST API 'session' endpoint does not have a target for logout all."
        raise NotImplementedError(error)

    def validate(self, **kwargs):
        """Send a validate request to check that token is still valid.

        Args:
            **kwargs:
                cause (:obj:`str`):
                    String to explain purpose of request.

                    Defaults to: "Validate token".

        Raises:
            :exc:`exceptions.NotLoggedInError`:
                If :attr:`CommonMixin.logged_in` is False.
            :exc:`exceptions.InvalidToken`:
                If status code in response is not 200.

        Returns:
            :obj:`str`

        """
        if not self.logged_in:
            raise exceptions.NotLoggedInError(auth_method=self)

        r = self.http_client(
            path="/api/v{v}/{e}".format(v=self.rest_version, e="session/validate"),
            method="post",
            data=json.dumps({"session": self._token}),
            timeout=self._login_timeout,
            cause=kwargs.pop("cause", "Validate token"),
        )

        if r.status_code != 200:
            raise exceptions.InvalidToken(auth_method=self, response=r)

        token = r.json()["data"]["session"]
        m = "Token validated for User ID {uid!r} from {url!r}"
        m = m.format(uid=self.uid, url=r.url)
        self.log.debug(m)
        self.token = token
        return token


def load(obj=DEFAULT_NAME):
    """Get an AuthMethod class.

    Args:
        obj (:obj:`str` or :obj:`AuthMethod` or :class:`AuthMethod` or
            :obj:`pytan3.auth_store.AuthStore`, optional):
            AuthStore object or AuthMethod object, class, or name of AuthMethod.

            Defaults to: :data:`DEFAULT_NAME`.

    Raises
        :exc:`exceptions.ModuleError`:
            If obj is not a valid type, name, obj, or cls.

    Returns:
        :class:`AuthMethod`

    """
    if isinstance(obj, auth_store.AuthStore):
        return obj.method

    if isinstance(obj, AuthMethod):
        return obj.__class__

    if callable(obj) and issubclass(obj, AuthMethod):
        return obj

    if isinstance(obj, six.string_types):
        for method_cls in AuthMethod.__subclasses__():
            if method_cls.get_name() == obj:
                return method_cls

    valids = [x.get_name() for x in AuthMethod.__subclasses__()]
    error = "{obj!r} is not a valid {cls}, try one of:\n  {valids}"
    error = error.format(obj=obj, cls=AuthMethod, valids=valids)
    raise exceptions.ModuleError(error)


def validate_token(token):
    """Validate that a token is properly formed.

    Args:
        token (:obj:`str`):
            Token to validate

    Returns:
        :obj:`bool`

    """
    return re.match(r"(\d+-\d+-)\w+", token) is not None

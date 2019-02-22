# -*- coding: utf-8 -*-
"""Clients for making API requests to Tanium."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import abc
import six
import warnings

from . import exceptions
from .. import utils

DEFAULT_NAME = "soap"
""":obj:`str`: Default :class:`ApiClient` name to load in :func:`load`."""

DEFAULT_TYPE = "soap"
""":obj:`str`: Default :class:`ApiClient` type to load in :func:`load_type`."""

WSDL_PATH = "/libraries/taniumjs/console.wsdl"
""":obj:`str`: URL path to find console.wsdl in :func:`get_wsdl`."""

warnings.simplefilter(action="once", category=exceptions.GetPlatformVersionWarning)
# only warn once about issues getting the platform version


@six.add_metaclass(abc.ABCMeta)
class ApiClient(object):
    """Abstract base class for all ApiClients."""

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
    def get_type(cls):
        """Get the ref type of this class for use by :func:`load_type`.

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

    @abc.abstractproperty
    def auth_method(self):
        """Get the AuthMethod for this object.

        Returns:
            :obj:`pytan3.auth_methods.AuthMethod`

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
    def url(self):
        """Get the URL from :attr:`ApiClient.http_client`.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def version(self):
        """Get the platform version from :attr:`ApiClient.config`.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def config(self):
        """Get the deserialized config.json from :attr:`ApiClient.url`.

        Returns:
            :obj:`dict`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def info(self):
        """Get the deserialized info.json from :attr:`ApiClient.url`.

        Returns:
            :obj:`dict`

        """
        raise NotImplementedError  # pragma: no cover


class Soap(ApiClient):
    """Client for making SOAP API requests to Tanium."""

    def __init__(self, http_client, auth_method, ver_check=True, lvl="info"):
        """Constructor.

        Args:
            http_client (:obj:`pytan3.http_client.HttpClient`):
                Object for sending HTTP requests.
            auth_method (:obj:`pytan3.auth_methods.AuthMethod`):
                Object for sending login and logout requests.
            ver_check (:obj:`bool`, optional):
                Perform version checks against the platform version from
                :attr:`ApiClient.version` using
                :func:`pytan3.utils.versions.version_check_obj_req`.

                Defaults to: True.
            lvl (:obj:`str`, optional):
                Logging level for this object.

                Defaults to: "info".

        """
        self.log = utils.logs.get_obj_log(obj=self, lvl=lvl)
        """:obj:`logging.Logger`: Log for this object."""
        self._auth_method = auth_method
        self._http_client = http_client
        if ver_check and any(self.get_version_req().values()):
            utils.versions.version_check_obj_req(
                version=self.version, src=self.url, obj=self
            )

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        bits = ["url={!r}".format(self.url), "type={!r}".format(self.get_type())]
        bits = "({})".format(", ".join(bits))
        cls = "{c.__module__}.{c.__name__}".format(c=self.__class__)
        return "{cls}{bits}".format(cls=cls, bits=bits)

    def __repr__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        return self.__str__()

    def __call__(self, data, timeout=30, **kwargs):
        """Get response of POST of data to /soap and return a response object.

        Args:
            data (:obj:`str`):
                Body to send in request.
            timeout (:obj:`int`, optional):
                Response timeout.

                Defaults to: 30.
            **kwargs:
                cause (:obj:`str`):
                    String to explain purpose of request.

                    Defaults to: "".
                headers (:obj:`dict`):
                    Headers to send in request.

                    Defaults to: {}.

        Returns:
            :obj:`requests.Response`

        """
        headers = kwargs.pop("headers", {}) or {}
        headers.update(self.auth_method.token_headers)
        r = self.http_client(
            method="post",
            path="/soap",
            data=data,
            headers=headers,
            timeout=timeout,
            cause=kwargs.pop("cause", ""),
        )
        return r

    @classmethod
    def get_name(cls):
        """Get the ref name of this object for use by :func:`load`.

        Returns:
            :obj:`str`

        """
        name = "soap"
        return name

    @classmethod
    def get_type(cls):
        """Get the ref type of this object for use by :func:`load_type`.

        Returns:
            :obj:`str`

        """
        return "soap"

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

    @property
    def auth_method(self):
        """Get the AuthMethod for this object.

        Returns:
            :obj:`pytan3.auth_methods.AuthMethod`

        """
        return self._auth_method

    @property
    def http_client(self):
        """Get the HTTP Client for this object.

        Returns:
            :obj:`pytan3.http_client.HttpClient`

        """
        return self._http_client

    @property
    def url(self):
        """Get the URL from :attr:`ApiClient.http_client`.

        Returns:
            :obj:`str`

        """
        return self.http_client.url

    @property
    def version(self):
        """Get the platform version from :attr:`ApiClient.config`.

        Returns:
            :obj:`str`

        """
        if not getattr(self, "_version", None):
            self._version = get_version(self.http_client)
        return self._version

    @property
    def config(self):
        """Get the deserialized config.json from :attr:`ApiClient.url`.

        Returns:
            :obj:`dict`

        """
        return get_config(self.http_client)

    @property
    def info(self):
        """Get the deserialized info.json from :attr:`ApiClient.url`.

        Returns:
            :obj:`dict`

        """
        return self.http_client(
            method="get",
            path="/info.json",
            headers=self.auth_method.token_headers,
            timeout=15,
        ).json()


class Rest(ApiClient):
    """Client for making REST API requests to Tanium for versions 7.3 and above."""

    def __init__(self, http_client, auth_method, ver_check=True, lvl="info"):
        """Constructor.

        Args:
            http_client (:obj:`pytan3.http_client.HttpClient`):
                Object for sending HTTP requests.
            auth_method (:obj:`pytan3.auth_methods.AuthMethod`):
                Object for sending login and logout requests.
            ver_check (:obj:`bool`, optional):
                Perform version checks against the platform version from
                :attr:`ApiClient.version` using
                :func:`pytan3.utils.versions.version_check_obj_req`.

                Defaults to: True.
            lvl (:obj:`str`, optional):
                Logging level for this object.

                Defaults to: "info".

        """
        self.log = utils.logs.get_obj_log(obj=self, lvl=lvl)
        """:obj:`logging.Logger`: Log for this object."""
        self._auth_method = auth_method
        self._http_client = http_client
        if ver_check and any(self.get_version_req().values()):
            utils.versions.version_check_obj_req(
                version=self.version, src=self.url, obj=self
            )

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        bits = ["url={!r}".format(self.url), "type={!r}".format(self.get_type())]
        bits = "({})".format(", ".join(bits))
        cls = "{c.__module__}.{c.__name__}".format(c=self.__class__)
        return "{cls}{bits}".format(cls=cls, bits=bits)

    def __repr__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        return self.__str__()

    def __call__(self, endpoint, method="get", data=None, timeout=30, **kwargs):
        """Get response of request of method to /api/v$version/$endpoint?$params.

        Args:
            endpoint (:obj:`str`):
                Endpoint of rest api
            method (:obj:`str`, optional):
                Method to use in request.

                Defaults to: "get".
            data (:obj:`str`, optional):
                Body to send in request.

                Defaults to: None
            timeout (:obj:`int`, optional):
                Response timeout.

                Defaults to: 30.
            **kwargs:
                cause (:obj:`str`):
                    String to explain purpose of request.

                    Defaults to: "".
                headers (:obj:`dict`):
                    Headers to send in request.

                    Defaults to: {}.
                version (:obj:`int`):
                    Version of REST API.

                    Defaults to: 2.
                params (:obj:`dict`):
                    Params to send encoded in URL.

                    Defaults to: {}.

        Returns:
            :obj:`requests.Response`

        """
        headers = kwargs.pop("headers", {}) or {}
        headers.update(self.auth_method.token_headers)
        version = kwargs.get("version", self.rest_version)
        r = self.http_client(
            method=method,
            data=data,
            path="/api/v{v}/{e}".format(v=version, e=endpoint),
            params=kwargs.pop("params", {}) or {},
            headers=headers,
            timeout=timeout,
            cause=kwargs.pop("cause", ""),
        )
        return r

    @classmethod
    def get_name(cls):
        """Get the ref name of this object for use by :func:`load`.

        Returns:
            :obj:`str`

        """
        name = "rest"
        return name

    @classmethod
    def get_type(cls):
        """Get the ref type of this object for use by :func:`load_type`.

        Returns:
            :obj:`str`

        """
        return "rest"

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

    @property
    def rest_version(self):
        """Get the API version to use when communicating with the REST API.

        Returns:
            :obj:`int`

        """
        return 2

    @property
    def auth_method(self):
        """Get the AuthMethod for this object.

        Returns:
            :obj:`pytan3.auth_methods.AuthMethod`

        """
        return self._auth_method

    @property
    def http_client(self):
        """Get the HTTP Client for this object.

        Returns:
            :obj:`pytan3.http_client.HttpClient`

        """
        return self._http_client

    @property
    def url(self):
        """Get the URL from :attr:`ApiClient.http_client`.

        Returns:
            :obj:`str`

        """
        return self.http_client.url

    @property
    def version(self):
        """Get the platform version from :attr:`ApiClient.config`.

        Returns:
            :obj:`str`

        """
        if not getattr(self, "_version", None):
            self._version = get_version(self.http_client)
        return self._version

    @property
    def config(self):
        """Get the deserialized config.json from :attr:`ApiClient.url`.

        Returns:
            :obj:`dict`

        """
        return get_config(self.http_client)

    @property
    def info(self):
        """Get the deserialized info.json from :attr:`ApiClient.url`.

        Returns:
            :obj:`dict`

        """
        return self.http_client(
            method="get",
            path="/info.json",
            headers=self.auth_method.token_headers,
            timeout=15,
        ).json()


def get_version(http_client):
    """Get serverVersion key from :func:`get_config`.

    Args:
        http_client (:obj:`pytan3.http_client.HttpClient`):
            Object for sending HTTP request.

    Raises:
        :exc:`exceptions.GetPlatformVersionWarning`:
            On error getting serverVersion key.

    Returns:
        :obj:`str`

    """
    cause = "Get platform version"
    try:
        return get_config(http_client=http_client, cause=cause)["serverVersion"]
    except Exception as exc:
        error = "Failed to get server version from url {url!r}, error: {exc}"
        error = error.format(url=http_client.url, exc=exc)
        warnings.warn(error, exceptions.GetPlatformVersionWarning)
        return ""


def get_wsdl(http_client):
    """Get response of GET to /libraries/taniumjs/console.wsdl.

    Args:
        http_client (:obj:`pytan3.http_client.HttpClient`):
            Object for sending HTTP request.

    Returns:
        :obj:`str`

    """
    path = WSDL_PATH
    return http_client(method="get", path=path, timeout=5).text


def get_config(http_client, cause=""):
    """Get response of GET to /config/console.json.

    Args:
        http_client (:obj:`pytan3.http_client.HttpClient`):
            Object for sending HTTP request.

    Returns:
        :obj:`dict`

    """
    path = "/config/console.json"
    return http_client(method="get", path=path, timeout=5, cause=cause).json()


def load_type(obj=DEFAULT_TYPE):
    """Get a :class:`ApiClient` by type from :meth:`ApiClient.get_type`.

    Args:
        obj (:obj:`str`, optional):
            ApiClient type to load.

            Defaults to: :data:`DEFAULT_TYPE`.

    Raises
        :exc:`exceptions.ModuleError`:
            Unable to find a valid :class:`ApiClient` with the supplied type.

    Returns:
        :class:`ApiClient`

    """
    exp_cls = ApiClient
    classes = exp_cls.__subclasses__()
    for cls in classes:
        if cls.get_type() == obj:
            return cls

    valids = list({x.get_type() for x in classes})
    error = "\n  ".join(
        ["", "{obj!r} is not a valid type of {cls}, try one of:", "types: {valids}"]
    )
    error = error.format(obj=obj, cls=exp_cls, valids=valids)
    raise exceptions.ModuleError(error)


def load(obj=DEFAULT_NAME):
    """Get a :class:`ApiClient` by name from :meth:`ApiClient.get_name`.

    Args:
        obj (:obj:`str` or :obj:`ApiClient` or :class:`ApiClient`, optional):
            ApiClient object, class, or name.

            Defaults to: :data:`DEFAULT_NAME`.

    Raises
        :exc:`exceptions.ModuleError`:
            Unable to find a valid :class:`ApiClient` with the supplied name.

    Returns:
        :class:`ApiClient`

    """
    exp_cls = ApiClient
    classes = exp_cls.__subclasses__()
    if isinstance(obj, exp_cls):
        return obj.__class__

    if callable(obj) and issubclass(obj, exp_cls):
        return obj

    if isinstance(obj, six.string_types):
        for cls in classes:
            if cls.get_name() == obj:
                return cls

    vnames = [x.get_name() for x in classes]
    error = "\n  ".join(
        ["", "{obj!r} is not a valid {cls}, try one of:", "names: {vn}"]
    )
    error = error.format(obj=obj, cls=exp_cls, vn=vnames)
    raise exceptions.ModuleError(error)

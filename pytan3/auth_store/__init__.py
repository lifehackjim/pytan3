# -*- coding: utf-8 -*-
"""Secure storage for Authentication methods."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import six
import warnings

from . import exceptions
from .. import utils
from .. import auth_methods

DEFAULT_NAME = "credentials"
""":obj:`str`: Default :class:`pytan3.auth_methods.AuthMethod` name to load in
:obj:`AuthStore`.
"""

STORE_FILE = utils.tools.get_env(
    key="PYTAN_STORE_FILE", default="{http_client.parsed_url.hostname}.store"
)
""":obj:`str`: Store filename template filename to use in :class:`AuthStore`.

Will use OS Environment variable "PYTAN_STORE_FILE" if set.
"""

STORE_SECRET = utils.tools.get_env(
    key="PYTAN_STORE_SECRET", default="B####VjNyMWx5ITFAbV9QcjB0M2N0M2QmSDFkZDNu"
)  # Default key to use for :obj:`AuthStore`.


class AuthStore(object):
    """Secure storage for :class:`pytan3.auth_methods.AuthMethod`."""

    def __init__(
        self,
        http_client,
        method=DEFAULT_NAME,
        secret=None,
        data=None,
        src="init",
        lvl="info",
    ):
        """Constructor.

        Args:
            http_client (:obj:`pytan3.http_client.HttpClient`):
                HTTP client.
            method (:obj:`str` or :class:`pytan3.auth_methods.AuthMethod`, optional):
                AuthMethod to use for this object.

                Defaults to: :data:`DEFAULT_NAME`.
            secret (:obj:`str`, optional):
                Encryption key.

                Will use STORE_SECRET as default if None.

                Defaults to: None.
            data (:obj:`dict`, optional):
                Initialize data store with dict.

                Defaults to: None.
            src (:obj:`str`, optional):
                Where this store came from.

                Defaults to: "init".
            lvl (:obj:`str`, optional):
                Logging level.

                Defaults to: "info".

        """
        secret = STORE_SECRET if secret is None else secret
        self._log = utils.logs.get_obj_log(obj=self, lvl=lvl)
        self._http_client = http_client
        self.__data = {}
        self.__data.update(data or {})
        self.src = src
        self.secret = secret
        self.method = method

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        bits = ["from={!r}".format(self.src)]
        bits = "({})".format(", ".join(bits))
        cls = "{c.__module__}.{c.__name__}".format(c=self.__class__)
        return "{cls}{bits}".format(cls=cls, bits=bits)

    def __repr__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        return self.__str__()

    @property
    def http_client(self):
        """Get the HTTP Client for this object.

        Returns:
            :obj:`pytan3.http_client.HttpClient`

        """
        return self._http_client

    def set(self, key, value):
        """Set key value in data.

        Args:
            key (:obj:`str`):
                Key name to set in data.
            value (:obj:`str`):
                Value to set for key in data.

        """
        self.__data[key] = value

    def get(self, key, required=True):
        """Get key value from data.

        Args:
            key (:obj:`str`):
                Key to get,
            required (:obj:`bool`, optional):
                Raise error if key not found in store.

                Defaults to: True.

        Raises:
            :exc:`exceptions.ModuleError`:
                If key is required and not found.

        Returns:
            :obj:`str`

        """
        try:
            return self.__data[key]
        except KeyError:
            if required:
                error = "No required key named {k!r} set for this AuthStore!"
                error = error.format(k=key)
                raise exceptions.ModuleError(error)
            else:
                return ""

    @property
    def secret(self):
        """Get the secret for this store.

        Returns:
            :obj:`str`

        """
        return self._build_key(http_client=self.http_client, secret=self.__secret)

    @secret.setter
    def secret(self, value):
        """Set the secret for this store.

        Args:
            value (:obj:`str`):
                secret to set.

        """
        self.__secret = value

    @property
    def method(self):
        """Get the method class for this store.

        Returns:
            :class:`pytan3.auth_methods.AuthMethod`

        """
        return auth_methods.load(self.get("METHOD", True))

    @method.setter
    def method(self, method=DEFAULT_NAME):
        """Set the method name for this store.

        Args:
            method (:obj:`str` or :class:`pytan3.auth_methods.AuthMethod`, optional):
                AuthMethod to use for this object.

                Defaults to: :data:`DEFAULT_NAME`.

        """
        self.set("METHOD", auth_methods.load(method).get_name())

    def create_method(self, **kwargs):
        """Create an :obj:`pytan3.auth_methods.AuthMethod` from this store.

        Args:
            **kwargs:
                Rest of kwargs passed to
                :func:`pytan3.auth_methods.AuthMethod.from_store`.

        Returns:
            :obj:`pytan3.auth_methods.AuthMethod`

        """
        return self.method.from_store(store=self, **kwargs)

    def to_stream(self, stream=None):
        """Write this stores encrypted data to a file like object.

        Args:
            stream (:obj:`io.IOBase`, optional):
                Object to write store to.

                If None, create and return a :obj:`six.StringIO`.

                Defaults to: None.

        Returns:
            :obj:`io.IOBase`

        """
        if stream is None:
            stream = six.StringIO()

        data = self._encrypt(
            data=self.__data, http_client=self.http_client, secret=self.__secret
        )
        stream.write(data)
        stream.seek(0)
        return stream

    def to_path(
        self, path=None, path_sub="stores", path_file=STORE_FILE, overwrite=False
    ):
        """Write this stores encrypted data to a path.

        Args:
            path (:obj:`str` or :obj:`pathlib.Path`, optional):
                Storage directory to use.
                If empty, resolve path via :func:`pytan3.utils.tools.get_storage_dir`.

                Defaults to: None.
            path_sub (:obj:`str`, optional):
                Sub directory under path that should contain path_file.

                Defaults to: "stores"
            path_file (:obj:`str`, optional):
                Filename to use for store file under path / path_sub.

                Defaults to: :data:`STORE_FILE`
            overwrite (:obj:`bool`, optional):
                If True, if store_file exists, overwrite and throw warning.

                If False, if store_file exists, do not overwrite and throw exception.

                If None, if store_file exists, do not overwrite and throw warning.

                Defaults to: False.

        Raises:
            :exc:`exceptions.ModuleError`:
                If path / path_sub / path_file exists and overwrite is False
            :exc:`exceptions.ModuleWarning`:
                If path / path_sub / path_file exists and overwrite is None or True.

        Returns:
            :obj:`pathlib.Path`:
                Absolute full path where store file was written.

        """
        path = utils.tools.get_storage_dir(path=path, path_sub=path_sub, mkdir=True)
        path = path / path_file.format(http_client=self.http_client)

        if path.is_file():
            pre = "overwrite is {overwrite!r} and store file {path!r} already exists"
            pre = pre.format(overwrite=overwrite, path=format(path))
            if overwrite is False:
                error = "{}, not overwriting".format(pre)
                raise exceptions.ModuleError(error)
            elif overwrite is None:
                error = "{}, not overwriting".format(pre)
                warnings.warn(error, exceptions.ModuleWarning)
                return path
            else:
                error = "{}, overwriting".format(pre)
                warnings.warn(error, exceptions.ModuleWarning)

        with path.open(mode="wt") as stream:
            stream = self.to_stream(stream=stream)
        path.chmod(0o600)
        return path

    def to_string(self):
        """Write this stores encrypted data to a string.

        Returns:
            :obj:`str`

        """
        stream = six.StringIO()
        stream = self.to_stream(stream=stream)
        data = stream.getvalue()
        stream.close()
        return data

    @classmethod
    def from_stream(cls, http_client, stream, secret=None, src="stream", lvl="info"):
        """Create store from encrypted data in a file like object.

        Args:
            http_client (:obj:`pytan3.http_client.HttpClient`):
                HTTP client.
            stream (:obj:`io.IOBase`):
                File like object to read from.
            secret (:obj:`str`, optional):
                Decryption key.

                Will use STORE_SECRET as default if None.

                Defaults to: None.
            src (:obj:`str`, optional):
                Where this store came from.

                Defaults to: "stream".
            lvl (:obj:`str`, optional):
                Logging level for this object.

                Defaults to: "info".

        Returns:
            :obj:`AuthStore`

        """
        secret = STORE_SECRET if secret is None else secret
        stream.seek(0)
        data = cls._decrypt(data=stream.read(), http_client=http_client, secret=secret)
        return cls(http_client=http_client, data=data, secret=secret, src=src, lvl=lvl)

    @classmethod
    def from_string(cls, http_client, string, secret=None, lvl="info"):
        """Create store from encrypted data in a string.

        Args:
            http_client (:obj:`pytan3.http_client.HttpClient`):
                HTTP client.
            string (:obj:`str`):
                String to read from.
            secret (:obj:`str`, optional):
                Decryption key.

                Will use STORE_SECRET as default if None.

                Defaults to: None.
            lvl (:obj:`str`, optional):
                Logging level for this object.

                Defaults to: "info".

        Returns:
            :obj:`AuthStore`

        """
        secret = STORE_SECRET if secret is None else secret
        stream = six.StringIO(string)
        store = cls.from_stream(
            http_client=http_client, stream=stream, secret=secret, src="string", lvl=lvl
        )
        stream.close()
        return store

    @classmethod
    def from_path(
        cls,
        http_client,
        path=None,
        path_sub="stores",
        path_file=STORE_FILE,
        secret=None,
        lvl="info",
    ):
        """Create store from encrypted data in a file.

        Args:
            http_client (:obj:`pytan3.http_client.HttpClient`):
                HTTP client.
            path (:obj:`str` or :obj:`pathlib.Path`, optional):
                Storage directory to use.
                If empty, resolve path via :func:`pytan3.utils.tools.get_storage_dir`.

                Defaults to: None.
            path_sub (:obj:`str`, optional):
                Sub directory under path that should contain path_file.

                Defaults to: "stores"
            path_file (:obj:`str`, optional):
                Filename to use for store file under path / path_sub.

                Defaults to: :data:`STORE_FILE`
            secret (:obj:`str`, optional):
                Decryption key.

                Will use STORE_SECRET as default if None.

                Defaults to: None.
            lvl (:obj:`str`, optional):
                Logging level for this object.

                Defaults to: "info".

        Raises:
            (:obj:`exceptions.ModuleError`):
                If path does not exist as a file.

        Returns:
            :obj:`AuthStore`

        """
        secret = STORE_SECRET if secret is None else secret
        path = utils.tools.get_storage_dir(path=path, path_sub=path_sub, mkdir=False)
        path = path / path_file.format(http_client=http_client)

        if not path.is_file():
            error = "File {path!r} does not exist, unable to read AuthStore data!"
            error = error.format(path=format(path))
            raise exceptions.ModuleError(error)
        with path.open(mode="rt") as stream:
            store = cls.from_stream(
                http_client=http_client,
                stream=stream,
                secret=secret,
                src="path",
                lvl=lvl,
            )
        return store

    # LATER(!) figure out once prompting land entered again
    # @classmethod
    # def from_prompts(
    #     cls,
    #     http_client,
    #     method=DEFAULT_NAME,
    #     secret=STORE_SECRET,
    #     prompt_method=True,
    #     lvl="info",
    # ):
    #     """Natch."""
    #     promptness = utils.prompts.promptness

    #     if prompt_method:
    #         ask = "Pick an authentication method:"
    #         choices = [x.get_name() for x in AuthMethod.__subclasses__()]
    #         method = promptness.ask_choice(ask, choices=choices, default=method)

    #     ask = "Use Custom Secret? "
    #     ask_secret = promptness.ask_bool(ask, default=False)
    #     if ask_secret:
    #         ask = "Custom secret:"
    #         secret = promptness.ask_str(ask, secure=True)

    #     method_cls = load(method)
    #     method_args = method_cls.get_args()
    #     req_args = method_cls.get_args_required()
    #     sec_args = method_cls.get_args_secure()
    #     store = cls(http_client=http_client, secret=secret, src="prompt", lvl=lvl)
    #     store.method = method_cls

    #     for arg in method_args:
    #         ask = "Provide {!r}".format(arg)
    #         value = promptness.ask_str(
    #             ask, default=None if arg in req_args else "", secure=arg in sec_args
    #         )
    #         store.set(key=arg, value=value)
    #     return store

    @classmethod
    def _decrypt(cls, data, http_client, secret=None):
        """Decrypt data using secret.

        Args:
            data (:obj:`str`):
                Data to decrypt.
            http_client (:obj:`pytan3.http_client.HttpClient`):
                HTTP client.
            secret (:obj:`str`, optional):
                Decryption key.

                Will use STORE_SECRET as default if None.

                Defaults to: None.

        Returns:
            :obj:`str`

        """
        secret = STORE_SECRET if secret is None else secret
        key = cls._build_key(http_client=http_client, secret=secret)
        data = six.ensure_text(data)[7:]
        data = utils.crypt.decrypt(data=data, key=key)
        return json.loads(data)

    @classmethod
    def _encrypt(cls, data, http_client, secret=None):
        """Encrypt data using secret.

        Args:
            data (:obj:`str`):
                Data to encrypt.
            http_client (:obj:`pytan3.http_client.HttpClient`):
                HTTP client.
            secret (:obj:`str`, optional):
                Decryption key.

                Will use STORE_SECRET as default if None.

                Defaults to: None.

        Returns:
            :obj:`str`

        """
        secret = STORE_SECRET if secret is None else secret
        key = cls._build_key(http_client=http_client, secret=secret)
        data = json.dumps(data)
        data = utils.crypt.encrypt(data=data, key=key)
        pre = "::CSC::" if secret == STORE_SECRET else "::CCC::"
        return "{}{}".format(pre, six.ensure_text(data))

    @classmethod
    def _build_key(cls, http_client, secret=None):
        """Build an encryption key by combining an SSL cert PEM and a secret.

        Args:
            http_client (:obj:`pytan3.http_client.HttpClient`):
                HTTP client.
            secret (:obj:`str`, optional):
                Decryption key.

                Will use STORE_SECRET as default if None.

                Defaults to: None.

        Returns:
            :obj:`str`

        """
        secret = STORE_SECRET if secret is None else secret
        if secret.startswith("B####"):
            secret = utils.tools.b64_decode(secret[5:])
        return "{}__{}".format(http_client.certify.store.pem, secret)

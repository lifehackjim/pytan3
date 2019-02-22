# -*- coding: utf-8 -*-
"""Client for making HTTP requests."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import cert_human
import datetime
import json
import re
import requests
import six
import warnings

from . import exceptions
from .. import utils
from .. import version

CERT_FILE = "{http_client.parsed_url.hostname}.pem"
""":obj:`str`: Certificate filename template for :meth:`Certify.__call__`."""

RECORD_FILE = "%Y_%m_%dT%H_%M_%S_%fZ.json"
""":obj:`str`: Record filename template for :meth:`HttpClient.response_hook_disk`."""

SHOW_CERT = "no"
""":obj:`bool`: Default prompt value for "Show full certificate info" in
:meth:`Certify.verify_hook`.

Will use OS Environment variable "PYTAN_SHOW_CERT" if set.
"""

SHOW_CHAIN = "no"
""":obj:`bool`: Default prompt value for "Show certificate chain info" in
:meth:`Certify.verify_hook`.

Will use OS Environment variable "PYTAN_SHOW_CHAIN" if set.
"""

CERT_VALID = "no"
""":obj:`bool`: Default prompt value for "Consider certificate valid" in
:meth:`Certify.verify_hook`.

Will use OS Environment variable "PYTAN_CERT_VALID" if set.
"""

cert_human.enable_urllib3_patch()
# enable urllib3 patch to attach certs to requests response objects


class HttpClient(object):
    """Convenience class for requests package."""

    CLEAN_HOOKS = {
        r"/auth": ["clean_hook_auth"],
        r"/api/v\d?/session": ["clean_hook_auth_rest"],
    }
    """:obj:`dict`: URL regex matches for cleaning bodies in cleaning hooks."""

    CLEAN_AUTH_KEYS = ["username", "password", "domain", "secondary"]
    """:obj:`list` of :obj:`str`: Keys to clean in cleaning hooks."""

    CLEAN_HIDE = "###HIDDEN###"
    """:obj:`str`: Text to use to hide values in cleaning hooks."""

    def __init__(self, url, timeout=5, lvl="info"):
        """Constructor.

        Args:
            url (:obj:`str`):
                URL to use.
            timeout (:obj:`int`, optional):
                Connect timeout to use for requests.

                Defaults to: 5.
            lvl (:obj:`str`, optional):
                Logging level for this object.

                Defaults to: "info".

        """
        self.log = utils.logs.get_obj_log(obj=self, lvl=lvl)
        """:obj:`logging.Logger`: Log for this object."""
        self.timeout = timeout
        """:obj:`int`: Connect timeout used for all requests."""
        self.parsed_url = self.parse_url(url)
        """:obj:`UrlParser`: Parsed version of URL."""
        self.last_request = None
        """:obj:`requests.PreparedRequest`: Last request sent."""
        self.last_response = None
        """:obj:`requests.Response`: Last response received."""
        self.history = []
        """:obj:`list`: History of all responses received.

        Used by :meth:`HttpClient.response_hook_history`.
        """
        self.record_path = None
        """:obj:`pathlib.Path`: Path to store response recordings to."""

        self.session = requests.Session()
        """:obj:`requests.Session`: Requests session object."""

        self.session.hooks = {"response": []}
        self.session.hooks["response"].append(self.response_hook_log_debug)
        self.session.hooks["response"].append(self.response_hook_clean)

        self.certify = Certify(http_client=self)
        """:obj:`Certify`: Certificate Magic object."""

    @property
    def url(self):
        """Get the URL string from :attr:`HttpClient.parsed_url`.

        Returns:
            :obj:`str`

        """
        return self.parsed_url.url

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        cert = self.certify.using_custom_cert
        cert = cert.name if cert else "None"
        bits = ["url={!r}".format(self.url), "cert={!r}".format(cert)]
        bits = "({})".format(", ".join(bits))
        cls = "{c.__module__}.{c.__name__}".format(c=self.__class__)
        return "{cls}{bits}".format(cls=cls, bits=bits)

    def __repr__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        return self.__str__()

    def __call__(
        self,
        method="get",
        path="",
        data=None,
        timeout=5,
        params=None,
        headers=None,
        b64_headers=None,
        verify=True,
        **kwargs
    ):
        """Create, prepare a request, and then send it.

        Args:
            method (:obj:`str`, optional):
                Method to use.

                Defaults to: "get".
            path (:obj:`str`, optional):
                Path to append to :attr:`HttpClient.url` for this request.

                Defaults to: "".
            data (:obj:`str`, optional):
                Data to send with POST.

                Defaults to: None.
            timeout (:obj:`int`, optional):
                Response timeout.

                Defaults to: 5.
            params (:obj:`dict`, optional):
                URL parameters.

                Defaults to: None.
            headers (:obj:`dict`, optional):
                Headers.

                Defaults to: None.
            b64_headers (:obj:`list` of :obj:`str`, optional):
                Headers to base 64 encode.

                Defaults to: None.
            verify (:obj:`bool` or :obj:`str`, optional):
                Enable/Disable SSL certificate validation using built in CAs,
                or a path to custom cert.

                Defaults to: True.
            **kwargs:
                cause (:obj:`str`): String to explain purpose of request.

                Defaults to: "".

        Notes:
            If verify is True or None, verification is done using default/built in
            CA. OS env vars $REQUESTS_CA_BUNDLE, and $CURL_CA_BUNDLE are used if set
            and trust_env is True, and if trust_env is False session's verify is used.

            If verify is False, no verification is done. This overrides OS env and
            session's verify for this request and no verification is done at all.
            Don't do this.

            If verify is a str, verification is done with PEM file at path.
            This overrides OS env and session's verify for this request.

            Caveat: If previous request made with session and close has not been
            called on session, the verify of the previous request will be used
            no matter what is supplied here.

        Returns:
            :obj:`requests.Response`

        """
        cause = kwargs.pop("cause", "")
        b64 = b64_headers or []

        h = {}
        h.update(headers or {})
        h.setdefault("User-Agent", self.user_agent)
        h.update({k: utils.tools.b64_encode(v) for k, v in h.items() if k in b64})

        req_args = {}
        req_args["url"] = requests.compat.urljoin(self.url, path)
        req_args["method"] = method
        req_args["data"] = data
        req_args["headers"] = h
        req_args["params"] = params

        send_args = {}
        send_args["timeout"] = (self.timeout, timeout)
        send_args.update(
            self.session.merge_environment_settings(
                url=self.url,
                proxies=None,  # rely on OS env proxies, then self.session.proxies
                stream=None,  # not using
                verify=verify,
                cert=None,  # rely on client cert set in self.session.cert
            )
        )

        request = requests.Request(**req_args)
        prequest = self.last_request = self.session.prepare_request(request=request)
        prequest.datetime = datetime.datetime.utcnow()
        prequest.cause = cause

        size = utils.tools.human_size(size=len(prequest.body or ""))
        m = "sent: url={p.url!r}, method={p.method!r}, size={size}"
        m = m.format(p=prequest, size=size)
        self.log.debug(m)

        r = self.last_response = self.session.send(prequest, **send_args)
        r.datetime = datetime.datetime.utcnow()
        r.cause = cause
        return r

    def control_hook(self, enable, hook):
        """Add or remove a hook from :attr:`HttpClient.session`.

        Args:
            enable (:obj:`bool`):
                True: Add hook to session.
                False: Remove hook from session.
            hook (:obj:`object`):
                Hook function to add/remove to session.

        Returns:
            :obj:`bool`:
                True/False if hook was actually removed/added.

        """
        ret = False
        self.session.hooks = getattr(self.session, "hooks", {}) or {}
        self.session.hooks["response"] = self.session.hooks.get("response", [])
        if enable:
            if hook not in self.session.hooks["response"]:
                self.session.hooks["response"].append(hook)
                ret = True
        else:
            if hook in self.session.hooks["response"]:
                self.session.hooks["response"].remove(hook)
                ret = True
        return ret

    def control_hook_record_disk(self, enable=False, path=None, path_sub="records"):
        """Add or remove session hook for recording responses to disk.

        Args:
            enable (:obj:`bool`, optional):
                Add/remove :meth:`HttpClient.response_hook_disk` to session hooks.

                Defaults to: False.
            path (:obj:`str` or :obj:`pathlib.Path`, optional):
                Storage directory to use.
                If empty, resolve path via :func:`pytan3.utils.tools.get_storage_dir`.

                Defaults to: None.
            path_sub (:obj:`str`, optional):
                Sub directory under path to save records to.

                Defaults to: "records"

        """
        path = utils.tools.get_storage_dir(path=path, path_sub=path_sub, mkdir=True)
        self.record_path = path
        if enable:
            done = self.control_hook(enable=True, hook=self.response_hook_disk)
            if done:
                m = "Started recording responses to {path!r}"
                m = m.format(path=format(path))
                self.log.debug(m)
        else:
            done = self.control_hook(enable=False, hook=self.response_hook_disk)
            if done:
                m = "Stopped recording responses to {path!r}"
                m = m.format(path=format(path))
                self.log.debug(m)

    def control_hook_record_history(self, enable=False):
        """Add or remove session hook for recording in local class.

        Args:
            enable (:obj:`bool`, optional):
                Add/remove :meth:`HttpClient.response_hook_history` to session hooks.

                Defaults to: False.

        """
        if enable:
            done = self.control_hook(enable=True, hook=self.response_hook_history)
            if done:
                m = "Started recording responses to {c!r}"
                m = m.format(c=format(self))
                self.log.debug(m)
        else:
            done = self.control_hook(enable=False, hook=self.response_hook_history)
            if done:
                m = "Stopped recording responses to {c!r}"
                m = m.format(c=format(self))
                self.log.debug(m)

    def response_hook_log_debug(self, response, *args, **kwargs):
        """Response hook to log info.

        Args:
            response (:obj:`requests.Response`):
                Response to process.
            *args:
                Unused, yet supplied by :obj:`requests.Session`.
            **kwargs:
                Unused, yet supplied by :obj:`requests.Session`.

        Returns:
            :obj:`requests.Response`

        """
        m = (
            "rcvd: url={response.url!r}, method={request.method!r}, size={size}, "
            "status={response.status_code!r}, reason={response.reason!r}, "
            "elapsed={response.elapsed}, cause={cause!r}"
        )
        m = m.format(
            response=response,
            request=response.request,
            size=utils.tools.human_size(len(response.text or "")),
            cause=getattr(response, "cause", ""),
        )
        self.log.debug(m)
        return response

    def response_hook_clean(self, response, *args, **kwargs):
        """Response hook to add cleaned versions of request/response body and headers.

        Args:
            response (:obj:`requests.Response`):
                Response to process.
            *args:
                Unused, yet supplied by :obj:`requests.Session`.
            **kwargs:
                Unused, yet supplied by :obj:`requests.Session`.

        Returns:
            :obj:`requests.Response`

        """
        response.clean_headers = response.headers or {}
        response.clean_body = response.text or ""
        response.request.clean_headers = response.request.headers or {}
        response.request.clean_body = response.request.body or ""

        for url, hooks in self.CLEAN_HOOKS.items():
            if not re.search(url, response.url):
                continue
            for hook in hooks:
                if isinstance(hook, six.string_types):
                    hook = getattr(self, hook, None)
                if callable(hook):
                    response = hook(http_client=self, response=response)
        return response

    @staticmethod
    def clean_hook_auth_rest(http_client, response):
        """Clean hook to hide auth keys in a response from REST session route.

        Args:
            http_client (:obj:`HttpClient`):
                Object to get :attr:`HttpClient.CLEAN_AUTH_KEYS` and
                :attr:`HttpClient.CLEAN_HIDE` from.
            response (:obj:`requests.Response`):
                Object to add clean_body attribute to.

        Returns:
            :obj:`requests.Response`

        """
        keys = http_client.CLEAN_AUTH_KEYS
        hidden = http_client.CLEAN_HIDE
        body = json.loads(response.request.clean_body)
        body = {k: hidden if k in keys else v for k, v in body.items()}
        response.request.clean_body = json.dumps(body, indent=2)
        return response

    @staticmethod
    def clean_hook_auth(http_client, response):
        """Clean hook to hide auth headers in a response from /auth API.

        Args:
            http_client (:obj:`HttpClient`):
                Object to get :attr:`HttpClient.CLEAN_AUTH_KEYS` and
                :attr:`HttpClient.CLEAN_HIDE` from.
            response (:obj:`requests.Response`):
                Object to add clean_headers attribute to.

        Returns:
            :obj:`requests.Response`

        """
        keys = http_client.CLEAN_AUTH_KEYS
        hidden = http_client.CLEAN_HIDE
        headers = response.request.clean_headers
        headers = {k: hidden if k in keys else v for k, v in headers.items()}
        response.request.clean_headers = headers
        return response

    def response_hook_history(self, response, *args, **kwargs):
        """Response hook to add response to :attr:`HttpClient.history`.

        Args:
            response (:obj:`requests.Response`):
                Response to process.
            *args:
                Unused, yet supplied by :obj:`requests.Session`.
            **kwargs:
                Unused, yet supplied by :obj:`requests.Session`.
        """
        self.history = getattr(self, "history", [])
        self.history.append(response)

    def response_hook_disk(self, response, *args, **kwargs):
        """Response hook to write response to :attr:`HttpClient.record_path`.

        Args:
            response (:obj:`requests.Response`):
                Response to serialize and write to disk.
            *args:
                Unused, yet supplied by :obj:`requests.Session`.
            **kwargs:
                Unused, yet supplied by :obj:`requests.Session`.

        Returns:
            :obj:`requests.Response`

        """
        self.record_path.mkdir(mode=0o700, parents=True, exist_ok=True)
        now = datetime.datetime.utcnow()
        record_file = getattr(response, "datetime", now).strftime(RECORD_FILE)
        record_path = self.record_path / record_file
        response.record_path = record_path
        with record_path.open("wb" if six.PY2 else "w") as fh:
            json.dump(obj=self.serialize_response(response), fp=fh, indent=2)
        m = "JSON record of response written to {path!r}"
        m = m.format(path=format(record_path))
        self.log.debug(m)
        return response

    def serialize_response(self, response):
        """Churn a response into JSON serializeable format.

        Args:
            response (:obj:`requests.Response`):
                Response object to churn.

        Returns:
            :obj:`dict`

        """
        request = response.request
        now = datetime.datetime.utcnow()
        ret = {
            "url": response.url,
            "url_path": request.path_url,
            "method": request.method,
            "elapsed": format(response.elapsed),
            "code": response.status_code,
            "cause": getattr(response.request, "cause", ""),
            "request": {
                "headers": dict(getattr(request, "clean_headers", request.headers)),
                "body": getattr(request, "clean_body", request.body),
                "datetime": format(getattr(request, "datetime", now)),
            },
            "response": {
                "headers": dict(getattr(response, "clean_headers", response.headers)),
                "body": getattr(response, "clean_body", response.text),
                "datetime": format(getattr(response, "datetime", now)),
            },
        }
        return ret

    def parse_url(self, url):
        """Parse a URL using UrlParser.

        Args:
            url (:obj:`str`):
                URL to parse.

        Returns:
            :obj:`UrlParser`

        """
        parsed_url = UrlParser(url=url, default_scheme="https")
        m = "Parsed url {old!r} into {new!r} using {parsed}"
        m = m.format(old=url, new=parsed_url.url, parsed=parsed_url)
        self.log.debug(m)
        return parsed_url

    @property
    def user_agent(self):
        """Build a user agent string for use in headers.

        Returns:
            :obj:`str`

        """
        return "{pkg}.{name}/{ver}".format(
            pkg=__name__.split(".")[0],
            name=self.__class__.__name__,
            ver=version.__version__,
        )


class Certify(object):
    """Certificate verification magic."""

    def __init__(self, http_client, lvl="info"):
        """Constructor.

        Args:
            http_client (:obj:`HttpClient`):
                Client to use for getting certificates and configuring the
                verify attribute on :attr:`HttpClient.session`
            lvl (:obj:`str`, optional):
                Logging level for this object.

                Defaults to: "info".

        """
        self.log = utils.logs.get_obj_log(obj=self, lvl=lvl)
        """:obj:`logging.Logger`: Logger for this object."""

        self.http_client = http_client
        """:obj:`HttpClient`: Client for this object."""

        self.using_custom_cert = False
        """:obj:`bool`: If we are using a cert from disk or not."""

    def __call__(
        self,
        path=None,
        path_sub="certs",
        path_file=CERT_FILE,
        verify_hook=None,
        overwrite=False,
        lvl=None,
    ):
        """Validate, find, or get certificate for URL.

        Args:
            path (:obj:`str` or :obj:`pathlib.Path`, optional):
                Storage directory to use.
                If empty, resolve path via :func:`pytan3.utils.tools.get_storage_dir`.

                Defaults to: None.
            path_sub (:obj:`str`, optional):
                Sub directory under path that should contain path_file.

                Defaults to: "certs"
            path_file (:obj:`str`, optional):
                Filename to use for cert file under path / path_sub.

                Defaults to: :attr:`CERT_FILE`
            verify_hook (:obj:`callable` or :obj:`False`):
                A callable used to verify a SSL cert from URL before writing it to disk.

                Only used if default cert is invalid and path/path_sub/path_file does
                not exist.

                If False, cert is written to disk without running any verify hook.

                If None, uses :meth:`Certify.verify_hook` as verify hook.

                If callable, called with args: store, store_chain, and parsed_url.

                Defaults to: None.
            overwrite (:obj:`bool`, optional):
                Overwrite cert at path if already exists.

                Defaults to: False.
            lvl (:obj:`str`, optional):
                If not None, change logging level for this object.

                Defaults to: None.

        Raises:
            :obj:`exceptions.CertificateNotFoundWarning`:
                If cert at URL is not valid using default cert validation,
                and no cert can be found at path.

        """
        utils.logs.set_level(lvl or self.log.level, self.log)
        if self.check_default():
            self.using_custom_cert = False
            return

        path = utils.tools.get_storage_dir(path=path, path_sub=path_sub, mkdir=False)
        path = path / path_file.format(http_client=self.http_client)
        path_is_file = path.is_file()

        if path_is_file:
            self.check_path(path=path)
            self.using_custom_cert = path
            return

        error = "\n".join(
            [
                "Unable to find certificate file for URL {url!r} at path {path!r}",
                "Will try to get certificate, prompt for verification, then write it.",
            ]
        )
        error = error.format(url=self.http_client.url, path=format(path))
        warnings.warn(error, exceptions.CertificateNotFoundWarning)

        if verify_hook is not False:
            if not verify_hook or not callable(verify_hook):
                verify_hook = self.verify_hook
            verify_hook(
                store=self.store,
                store_chain=self.store_chain,
                parsed_url=self.http_client.parsed_url,
            )

        self.write_pem(path=path, overwrite=overwrite)
        self.using_custom_cert = path

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        bits = ["custom_cert={!r}".format(format(self.using_custom_cert))]
        bits = "({})".format(", ".join(bits))
        cls = "{c.__module__}.{c.__name__}".format(c=self.__class__)
        return "{cls}{bits}".format(cls=cls, bits=bits)

    def __repr__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        return self.__str__()

    def write_pem(self, path, overwrite=False):
        """Write a certificate in PEM format to disk.

        Args:
            path (:obj:`str` or :obj:`pathlib.Path`):
                Path to write PEM certificate to.
            overwrite (:obj:`bool`, optional):
                Overwrite cert at path if already exists.

                Defaults to: False.

        Returns:
            :obj:`pathlib.Path`

        """
        path = self.store.to_path(path=path, overwrite=overwrite)
        m = "Wrote certificate for {url!r} to {path!r}"
        m = m.format(url=self.http_client.url, path=format(path))
        self.log.debug(m)
        self.check_path(path=path)
        return path

    @staticmethod
    def verify_hook(store, store_chain, parsed_url):
        """Verify cert by prompting user, default hook.

        Args:
            store (:obj:`cert_human.CertStore`):
                Store from :attr:`Certify.store`.
            store_chain (:obj:`cert_human.CertChainStore`):
                Chain store from :attr:`Certify.store_chain`.
            parsed_url (:obj:`str`):
                Parsed URL from :attr:`HttpClient.parsed_url`.

        Raises:
            :exc:`exceptions.CertificateInvalidError`:
                If user replies No to validity prompt.

        """
        promptness = utils.prompts.Promptness()

        text = "\n{{f.yellow}}Validating certificate from URL: {url!r}{{s.reset}}\n"
        text = text.format(url=parsed_url.url)
        promptness.spew(text=promptness.prepare(text=text))

        text = "{f.cyan}Brief certificate info:{s.reset}\n"
        promptness.spew(text=promptness.prepare(text=text))
        promptness.spew(text=store.dump_str_info)

        show_all = promptness.ask_bool(
            text="Show full certificate info?",
            default=SHOW_CERT,
            env_var="PYTAN_SHOW_CERT",
        )

        if show_all:
            text = "{f.cyan}Full certificate info:{s.reset}\n"
            promptness.spew(text=promptness.prepare(text=text))
            promptness.spew(text=store.dump_str)

        show_chain = promptness.ask_bool(
            text="Show certificate chain?",
            default=SHOW_CHAIN,
            env_var="PYTAN_SHOW_CHAIN",
        )

        if show_chain:
            text = "{f.cyan}Certificate chain:{s.reset}\n"
            promptness.spew(text=promptness.prepare(text=text))
            promptness.spew(text=store_chain.dump_str_info)

        valid = promptness.ask_bool(
            text="Is this certificate valid?",
            default=CERT_VALID,
            env_var="PYTAN_CERT_VALID",
        )

        if valid:
            return
        error = "User said certificate from URL {u!r} is invalid! Certificate:\n{c}"
        error = error.format(u=parsed_url.url, c=store.dump_str_info)
        raise exceptions.CertificateInvalidError(error)

    @property
    def store(self):
        """Get CertStore for URL.

        Returns:
            :obj:`cert_human.CertStore`

        """
        self._fetch_stores
        return self._store

    @property
    def store_chain(self):
        """Get CertChainStore for URL.

        Returns:
            :obj:`cert_human.CertChainStore`

        """
        self._fetch_stores
        return self._store_chain

    @property
    def _fetch_stores(self):
        """Get the CertStore and CertChainStore for URL.

        Returns:
            (:obj:`cert_human.CertStore`, :obj:`cert_human.CertChainStore`)

        """
        attrs = ["_store", "_store_chain"]
        if not any(getattr(self, x, None) for x in attrs):
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                # close all ctx so previous verify not used
                self.http_client.session.close()
                cause = "Get certs for certify stores"
                r = self.http_client(verify=False, cause=cause)
                # close all ctx so future verify does not use False
                self.http_client.session.close()
            self._store = cert_human.CertStore.from_response(response=r)
            self._store_chain = cert_human.CertChainStore.from_response(response=r)
        return (self._store, self._store_chain)

    def check_default(self):
        """Check if cert for URL is valid without setting a specific path.

        Returns:
            :obj:`bool`

        """
        # close all ctx so previous verify not used
        self.http_client.session.close()

        m = "Checking that default certificate is valid for URL {url!r}."
        m = m.format(url=self.http_client.url)
        self.log.debug(m)

        m = "Certificate Info for {url!r}:\n{info}"
        m = m.format(url=self.http_client.url, info=self.store.dump_str_info)
        self.log.debug(m)

        cause = "Test default cert of peer"
        try:
            self.http_client(verify=True, cause=cause)
            # close all ctx so future verify do not use True
            self.http_client.session.close()
            m = "Default certificate for {url!r} is valid, not setting custom cert."
            m = m.format(url=self.http_client.url)
            self.log.debug(m)
            return True
        except requests.exceptions.SSLError as exc:
            m = "Default certificate for {url!r} is not valid, will find/get one."
            m = m.format(url=self.http_client.url)
            self.log.debug(m)
            m = "Default certificate error: {exc}".format(exc=exc)
            self.log.debug(m)
            return False

    def check_path(self, path):
        """Check if cert at path is valid for URL.

        Args:
            path (:obj:`str` or :obj:`pathlib.Path`):
                Path to PEM certificate file.

        Notes:
            If validation is successful, the verify attribute on
            :attr:`HttpClient.session` will be set to path.

        Raises:
            :exc:`exceptions.CertificateInvalidError`:
                If path fails verification.

        """
        # close all ctx so previous verify not used
        self.http_client.session.close()

        m = "Checking that certificate at {path!r} is valid for URL {url!r}."
        m = m.format(path=format(path), url=self.http_client.url)
        self.log.debug(m)

        cause = "Test custom cert at {!r}".format(format(path))
        try:
            self.http_client(verify=format(path), cause=cause)
        except requests.exceptions.SSLError as exc:
            # close all ctx so future ctx dont use test verify
            self.http_client.session.close()
            m = "Certificate error: {exc}".format(exc=exc)
            self.log.debug(m)

            error = "Certificate at {path!r} is not valid for URL {url!r}"
            error = error.format(path=format(path), url=self.http_client.url)
            raise exceptions.CertificateInvalidError(error)

        m = (
            "Certificate at {path!r} is valid for URL {url!r}, "
            "will use for SSL verification."
        )
        m = m.format(path=format(path), url=self.http_client.url)
        self.log.debug(m)

        self.http_client.session.verify = format(path)
        # close all ctx so future ctx use new verify
        self.http_client.session.close()


class UrlParser(object):
    """Parse a URL and ensure it has the neccessary bits."""

    def __init__(self, url, default_scheme=""):
        """Constructor.

        Args:
            url (:obj:`str`):
                URL to parse
            default_scheme (:obj:`str`, optional):
                If no scheme in URL, use this.

                Defaults to: ""

        Raises:
            :exc:`exceptions.ModuleError`:
                If parsed URL winds up without a hostname, port, or scheme.

        """
        self._init_url = url
        """:obj:`str`: Initial URL provided."""
        self._init_scheme = default_scheme
        """:obj:`str`: Default scheme provided."""
        self._init_parsed = requests.compat.urlparse(url)
        """:obj:`urllib.parse.ParseResult`: First pass of parsing URL."""
        self.parsed = self.reparse(
            parsed=self._init_parsed, default_scheme=default_scheme
        )
        """:obj:`urllib.parse.ParseResult`: Second pass of parsing URL."""

        for part in ["hostname", "port", "scheme"]:
            if not getattr(self.parsed, part, None):
                error = "\n".join(
                    [
                        "",
                        "Parsed into: {pstr}",
                        "URL format should be like: scheme://hostname:port",
                        "No {part} provided in URL {url!r}",
                    ]
                )
                error = error.format(part=part, url=url, pstr=self.parsed_str)
                raise exceptions.ModuleError(error)

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        bits = ["parsed={!r}".format(self.parsed_str)]
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
    def hostname(self):
        """Hostname part from :attr:`UrlParser.parsed`.

        Returns:
            :obj:`str`

        """
        return self.parsed.hostname

    @property
    def port(self):
        """Port part from :attr:`UrlParser.parsed`.

        Returns:
            :obj:`int`

        """
        return int(self.parsed.port)

    @property
    def scheme(self):
        """Scheme part from :attr:`UrlParser.parsed`.

        Returns:
            :obj:`str`

        """
        return self.parsed.scheme

    @property
    def url(self):
        """Get scheme, hostname, and port from :attr:`UrlParser.parsed`.

        Returns:
            :obj:`str`

        """
        return self.unparse_base(p=self.parsed)

    @property
    def url_full(self):
        """Get full URL from :attr:`UrlParser.parsed`.

        Returns:
            :obj:`str`

        """
        return self.unparse_all(p=self.parsed)

    @property
    def parsed_str(self):
        """Create string of :attr:`UrlParser.parsed`.

        Returns:
            :obj:`str`

        """
        parsed = getattr(self, "parsed", None)
        attrs = [
            "scheme",
            "netloc",
            "hostname",
            "port",
            "path",
            "params",
            "query",
            "fragment",
        ]
        vals = ", ".join(
            [
                "{a}={v!r}".format(a=a, v="{}".format(getattr(parsed, a, "")) or "")
                for a in attrs
            ]
        )
        return vals

    def make_netloc(self, host, port):
        """Create netloc from host and port.

        Args:
            host (:obj:`str`):
                Host part to use in netloc.
            port (:obj:`str`):
                Port part to use in netloc.

        Returns:
            :obj:`str`

        """
        netloc = ":".join([host, port]) if port else host
        return netloc

    def reparse(self, parsed, default_scheme=""):
        """Reparse a parsed URL into a parsed URL with values fixed.

        Args:
            parsed (:obj:`urllib.parse.ParseResult`):
                Parsed URL to reparse.
            default_scheme (:obj:`str`, optional):
                If no scheme in URL, use this.

                Defaults to: ""

        Returns:
            :obj:`urllib.parse.ParseResult`

        """
        scheme, netloc, path, params, query, fragment = parsed
        host = parsed.hostname
        port = format(parsed.port or "")

        if not netloc and scheme and path and path.split("/")[0].isdigit():
            """For case:
            >>> urllib.parse.urlparse('host:443/')
            ParseResult(
                scheme='host', netloc='', path='443/', params='', query='', fragment=''
            )
            """
            host = scheme  # switch host from scheme to host
            port = path.split("/")[0]  # remove / from path and assign to port
            path = ""  # empty out path
            scheme = default_scheme
            netloc = ":".join([host, port])

        if not netloc and path:
            """For cases:
            >>> urllib.parse.urlparse('host:443')
            ParseResult(
                scheme='', netloc='', path='host:443', params='', query='', fragment=''
            )
            >>> urllib.parse.urlparse('host')
            ParseResult(
                scheme='', netloc='', path='host', params='', query='', fragment=''
            )
            """
            netloc, path = path, netloc
            if ":" in netloc:
                host, port = netloc.split(":", 1)
                netloc = ":".join([host, port]) if port else host
            else:
                host = netloc

        scheme = scheme or default_scheme
        if not scheme and port:
            if format(port) == "443":
                scheme = "https"
            elif format(port) == "80":
                scheme = "http"

        if not port:
            if scheme == "https":
                port = "443"
                netloc = self.make_netloc(host, port)
            elif scheme == "http":
                port = "80"
                netloc = self.make_netloc(host, port)

        pass2 = requests.compat.urlunparse(
            (scheme, netloc, path, params, query, fragment)
        )
        ret = requests.compat.urlparse(pass2)
        return ret

    def unparse_base(self, p):
        """Unparse a parsed URL into just the scheme, hostname, and port parts.

        Args:
            p (:obj:`urllib.parse.ParseResult`):
                Parsed URL to unparse.

        Returns:
            :obj:`str`

        """
        # only unparse self.parsed into url with scheme and netloc
        return requests.compat.urlunparse((p.scheme, p.netloc, "", "", "", ""))

    def unparse_all(self, p):
        """Unparse a parsed URL with all the parts.

        Args:
            p (:obj:`urllib.parse.ParseResult`):
                Parsed URL to unparse.

        Returns:
            :obj:`str`

        """
        return requests.compat.urlunparse(p)

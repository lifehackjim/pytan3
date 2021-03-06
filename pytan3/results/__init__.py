# -*- coding: utf-8 -*-
"""Result objects that deserialize responses from Tanium API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import abc

import json
import re
import six

from six.moves import urllib
import xmltodict

from . import exceptions
from .. import utils


@six.add_metaclass(abc.ABCMeta)
class Result(object):
    """Deserialize API responses from Tanium API."""

    @classmethod
    @abc.abstractmethod
    def from_response(cls, api_objects, response, lvl="info"):
        """Create :obj:`Result` from :obj:`requests.Response`.

        Args:
            api_objects (:obj:`pytan3.api_objects.ApiObjects`):
                API Objects Container to use.
            response (:obj:`requests.Response`):
                Response object received from Tanium API request.
            lvl (:obj:`str`, optional):
                Logging level.

                Defaults to: "info".

        Returns:
            :obj:`Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def error_check(self):
        """Check for errors in :attr:`response_body_str`.

        Raises:
            :exc:`exceptions.ObjectExistsError`
            :exc:`exceptions.ObjectNotFoundError`
            :exc:`exceptions.ResponseError`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def error_text(self):
        """Get the error text from :attr:`response_body_str`.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def api_objects(self):
        """Get the API objects container.

        Returns:
            :obj:`pytan3.api_objects.ApiObjects`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def url(self):
        """Get the URL used in request.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def status_code(self):
        """Get the status code received in response.

        Returns:
            :obj:`int`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def method(self):
        """Get the method used in request.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def request_body_str(self):
        """Get the full request body.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def request_body_obj(self):
        """Get :attr:`request_body_str` deserialized into a python object.

        Returns:
            :obj:`object`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def request_object_obj(self):
        """Get the request objects from :attr:`request_body_obj`.

        Returns:
            :obj:`dict`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def response_body_str(self):
        """Get the full response body.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def response_body_obj(self):
        """Get :attr:`response_body_str` deserialized into a python object.

        Returns:
            :obj:`object`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def data_obj(self):
        """Get the response data from :attr:`response_body_obj`.

        Returns:
            :obj:`object`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def data_api(self, **kwargs):
        """Get :attr:`data_obj` deserialized into an ApiModel object.

        Returns:
            :obj:`pytan3.api_models.ApiModel`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def object_obj(self):
        """Get the response objects from :attr:`response_body_obj`.

        Returns:
            :obj:`dict`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def object_api(self, **kwargs):
        """Get :attr:`object_obj` deserialized into an ApiModel object.

        Returns:
            :obj:`pytan3.api_models.ApiModel`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def str_to_obj(self, text, src, **kwargs):
        """Deserialize string into a python object.

        Args:
            text (:obj:`str`):
                String to decode into python object
            src (:obj:`str`):
                Where text came from, used in error text.

        Raises:
            :exc:`exceptions.TextDeserializeError`:

        Returns:
            :obj:`object`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def obj_to_api(self, obj, src):
        """Deserialize a python object into :obj:`pytan3.api_models.ApiModel`.

        Args:
            obj (:obj:`object`):
                Python object to deserialize into a PyTan API object.
            src (:obj:`str`):
                Where obj came from, used in error text.

        Returns:
            :obj:`pytan3.api_models.ApiModel`

        """
        raise NotImplementedError  # pragma: no cover


class CommonMixin(object):
    """Shared methods common amongst all :class:`Result`."""

    def __init__(
        self,
        api_objects,
        response_body,
        request_body,
        method,
        url,
        status_code,
        origin=None,
        lvl="info",
    ):
        """Constructor.

        Args:
            api_objects (:obj:`pytan3.api_objects.ApiObjects`):
                API Objects Container to use.
            response_body (:obj:`str`):
                Response body received from Tanium API.
            request_body (:obj:`str`):
                Request body sent to Tanium API.
            method (:obj:`str`):
                HTTP method used in request to Tanium API.
            url (:obj:`str`):
                URL used in request to Tanium API.
            status_code (:obj:`int`):
                Status code in response from Tanium API.
            origin (:obj:`requests.Response`, optional):
                Original response object received from Tanium API request.

                Defaults to: None.
            lvl (:obj:`str`, optional):
                Logging level.

                Defaults to: "info".

        """
        self.log = utils.logs.get_obj_log(obj=self, lvl=lvl)
        """:obj:`logging.Logger`: Log for this object."""
        self._api_objects = api_objects
        self._response_body_str = response_body
        self._request_body_str = request_body
        self._method = method
        self._url = url
        self._status_code = status_code
        self._cache = {}
        self.origin = origin
        """:obj:`requests.Response`: Original response object."""

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        bits = [
            "api_objects={!r}".format(self.api_objects),
            "url={!r}".format(self.url),
            "method={!r}".format(self.method),
            "code={!r}".format(self.status_code),
        ]
        bits = "(\n  {},\n)".format(",\n  ".join(bits))
        cls = "{c.__module__}.{c.__name__}".format(c=self.__class__)
        return "{cls}{bits}".format(cls=cls, bits=bits)

    def __repr__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        return self.__str__()

    @classmethod
    def from_response(cls, api_objects, response, lvl="info"):
        """Create Result from a requests response object.

        Args:
            api_objects (:obj:`pytan3.api_objects.ApiObjects`):
                API Objects Container to use.
            response (:obj:`requests.Response`):
                Response object received from Tanium API request.
            lvl (:obj:`str`, optional):
                Logging level.

                Defaults to: "info".

        Returns:
            :obj:`Result`

        """
        return cls(
            api_objects=api_objects,
            response_body=response.text,
            request_body=response.request.body,
            method=response.request.method,
            url=response.url,
            status_code=response.status_code,
            origin=response,
            lvl=lvl,
        )

    @property
    def api_objects(self):
        """Get the API objects container.

        Returns:
            :obj:`pytan3.api_objects.ApiObjects`

        """
        return self._api_objects

    @property
    def url(self):
        """Get the URL used in request.

        Returns:
            :obj:`str`

        """
        return self._url

    @property
    def status_code(self):
        """Get the status code received in response.

        Returns:
            :obj:`int`

        """
        return int(self._status_code)

    @property
    def method(self):
        """Get the method used in request.

        Returns:
            :obj:`str`

        """
        return self._method

    @property
    def request_body_str(self):
        """Get the full request body.

        Returns:
            :obj:`str`

        """
        return self._request_body_str or ""

    @property
    def response_body_str(self):
        """Get the full response body.

        Returns:
            :obj:`str`

        """
        return self._response_body_str or ""

    def obj_to_api(self, api_name, obj, src):
        """Deserialize a python object into :obj:`pytan3.api_models.ApiModel`.

        Args:
            api_name (:obj:`str`):
                API name of obj.
            obj (:obj:`object`):
                Python object to deserialize into a PyTan API object.
            src (:obj:`str`):
                Where obj came from, used in error text.

        Returns:
            :obj:`pytan3.api_models.ApiModel`

        """
        cls = self.api_objects.cls_by_name(name=api_name)
        with utils.tools.Timer() as t:
            if cls.__name__ == "ClientCount":
                ret = cls(count=obj)
            elif isinstance(obj, (list, tuple)):
                ret = cls(*obj)
            elif isinstance(obj, dict):
                ret = cls(**obj)
            # LATER(!) raise exc
        m = "Deserialized API name {a} obj type {t} from API into {cls!r}, took {e}"
        m = m.format(a=api_name, t=type(obj), cls=ret.__class__, e=t.elapsed)
        self.log.debug(m)
        return ret

    def get_dict_path(self, obj, path, src):
        """Traverse a dict using a / seperated string.

        Args:
            obj (:obj:`dict`):
                Dictionary to traverse using path.
            path (:obj:`str`):
                Nested dictionary keys seperated by / to traverse in obj.
            src (:obj:`str`):
                Where obj came from, used in error text.

        Raises:
            :exc:`exceptions.DictionaryPathError`:
                If any error occurs while traversing path in obj.

        Returns:
            :obj:`object`

        """
        try:
            ret = utils.tools.get_dict_path(obj=obj, path=path)
        except Exception as exc:
            raise exceptions.DictionaryPathError(
                result=self, obj=obj, path=path, src=src, exc=exc
            )
        return ret


class Soap(CommonMixin, Result):
    """Deserialize SOAP API responses from Tanium API."""

    DATA_ROUTES = ["GetResultInfo", "GetResultData", "GetMergedResultData"]

    def __call__(self, raw=False, **kwargs):
        """Get :attr:`data_api` or :attr:`object_api`.

        Args:
            raw (:obj:`bool`, optional):
                Return the serialized object instead of the object deserialized into
                an ApiModel.

                Defaults to: False.
            **kwargs:
                rest of kwargs:
                    passed to :meth:`object_api` or :meth:`data_api`.

        Notes:
            Will return :meth:`object_api` or :meth:`data_api` by
            determining if :attr:`command_request` is an object or data request.

        Returns:
            :obj:`pytan3.api_models.ApiModel` or :obj:`object`

        """
        self.error_check()
        is_result_data = self.command_request in self.DATA_ROUTES
        if is_result_data:
            _raw = self.data_obj
            _api = self.data_api
        else:
            _raw = self.object_obj
            _api = self.object_api
        return _raw if raw else _api(**kwargs)

    @property
    def error_map(self):
        """Map of status codes to regex patterns and exceptions.

        Notes:
            Keys should be :obj:`int` of a status code to check patterns of.

            Values should be :obj:`list` of [pattern, exc], where pattern is a regex
            pattern to search response body, and exc is exception to throw if pattern
            match is found.

        Raises:
            :exc:`exceptions.ObjectExistsError`
            :exc:`exceptions.ObjectNotFoundError`
            :exc:`exceptions.ResponseError`

        Returns:
            :obj:`dict`

        """
        ret = {}
        ret[200] = [
            [r"400.*already.*exists", exceptions.ObjectExistsError],
            [r"NotUnique", exceptions.ObjectExistsError],
            [r"400.*not.*found", exceptions.ObjectNotFoundError],
            [r"404.*not.*found", exceptions.ObjectNotFoundError],
        ]
        return ret

    def error_check(self):
        """Check for errors in :attr:`CommonMixin.response_body_str`.

        Raises:
            :exc:`exceptions.ObjectExistsError`
            :exc:`exceptions.ObjectNotFoundError`
            :exc:`exceptions.ResponseError`

        """
        self.error_check_response()
        self.error_check_code()

    def error_check_response(self):
        """Check :attr:`Soap.command_response` for errors.

        Notes:
            For each key value pair in :attr:`error_map`, if key matches
            :attr:`CommonMixin.status_code` or key is None, the patterns in value are
            checked against response body, and if matched the patterns associated
            exception is thrown.

        """
        for code, checks in self.error_map.items():
            if code is None or self.status_code == code:
                for check in checks:
                    pattern, error_exc = check
                    pattern_re = re.compile(pattern, re.IGNORECASE | re.DOTALL)
                    found = pattern_re.search(self.command_response)
                    if found:
                        raise error_exc(result=self, error=self.error_text)

        if self.command_request != self.command_response:
            error = "Request {req!r} does not match response:\n{resp}"
            error = error.format(resp=self.error_text, req=self.command_request)
            raise exceptions.ResponseError(self, error)

    def error_check_code(self):
        """Check if :attr:`CommonMixin.status_code` is one of :attr:`valid_codes`.

        Raises:
            :exc:`exceptions.ResponseError`

        """
        if self.status_code not in self.valid_codes:
            error = "Response status code {c} is not one of {v}, error text:\n{e}"
            error = error.format(
                c=self.status_code, v=self.valid_codes, e=self.error_text
            )
            raise exceptions.ResponseError(result=self, error=error)

    @property
    def valid_codes(self):
        """List of valid status codes.

        Returns:
            :obj:`list` of :obj:`int`

        """
        return [200]

    @property
    def error_text(self):
        """Get the error text from :attr:`CommonMixin.response_body_str`.

        Returns:
            :obj:`str`

        """
        return ", ".join([x for x in self.command_response.splitlines() if x])

    @property
    def command_request(self):
        """Get the "command" element from :attr:`request_body_obj`.

        Returns:
            :obj:`str`

        """
        obj = self.request_body_obj
        path = "soap:Envelope/soap:Body/t:tanium_soap_request/command"
        src = "SOAP API deserialized request body"
        return self.get_dict_path(obj=obj, path=path, src=src)

    @property
    def command_response(self):
        """Get the "command" element from :attr:`response_body_obj`.

        Returns:
            :obj:`str`

        """
        obj = self.response_body_obj
        path = "soap:Envelope/soap:Body/t:return/command"
        src = "SOAP API deserialized response body"
        return self.get_dict_path(obj=obj, path=path, src=src)

    @property
    def request_body_obj(self):
        """Deserialize :attr:`CommonMixin.request_body_str` into a python object.

        Returns:
            :obj:`dict`

        """
        key = "request_body_obj"
        if key not in self._cache:
            text = self.request_body_str
            src = "SOAP API request body"
            self._cache[key] = self.str_to_obj(
                text=text, src=src, try_int=True, use_dict=True, flat_attrs=True
            )
        return self._cache[key]

    @property
    def request_object_obj(self):
        """Get the request objects from :attr:`request_body_obj`.

        Returns:
            :obj:`dict`

        """
        obj = self.request_body_obj
        path = "soap:Envelope/soap:Body/t:tanium_soap_request/object_list"
        src = "SOAP API deserialized request body"
        return self.get_dict_path(obj=obj, path=path, src=src)

    @property
    def response_body_obj(self):
        """Get :attr:`CommonMixin.response_body_str` deserialized into a python object.

        Returns:
            :obj:`dict`

        """
        key = "response_body_obj"
        if key not in self._cache:
            text = self.response_body_str
            src = "SOAP API response body"
            self._cache[key] = self.str_to_obj(
                text=text, src=src, try_int=True, use_dict=True, flat_attrs=True
            )
        return self._cache[key]

    @property
    def data_xml(self):
        """Get the "ResultXML" element from :attr:`response_body_obj`.

        Returns:
            :obj:`str`

        """
        obj = self.response_body_obj
        path = "soap:Envelope/soap:Body/t:return/ResultXML"
        src = "SOAP API deserialized response body"
        data = self.get_dict_path(obj=obj, path=path, src=src)
        return data or ""

    @property
    def data_obj(self):
        """Get the response data from :attr:`data_xml`.

        Returns:
            :obj:`object`

        """
        key = "data_obj"
        if key not in self._cache:
            text = self.data_xml
            src = "'ResultXML' element from SOAP API deserialized response body"
            self._cache[key] = self.str_to_obj(
                text=text, src=src, try_int=False, use_dict=True, flat_attrs=True
            )
        return self._cache[key]

    def data_api(self, **kwargs):
        """Get :attr:`data_obj` deserialized into an ApiModel object.

        Args:
            **kwargs:
                rest of kwargs:
                    passed to :meth:`CommonMixin.obj_to_api`

        Returns:
            :obj:`pytan3.api_models.ApiModel`

        """
        if self.command_request not in self.DATA_ROUTES:
            error = "Route {req!r} is not one of {data}, not a data request?"
            error = error.format(req=self.command_request, data=self.DATA_ROUTES)
            raise exceptions.ApiWrongRequestType(result=self, error=error)

        kwargs["src"] = "Result data from 'ResultXML' element in SOAP response"
        kwargs["api_name"] = list(self.data_obj.keys())[0]
        kwargs["obj"] = list(self.data_obj.values())[0]
        return self.obj_to_api(**kwargs)

    @property
    def object_obj(self):
        """Get the response objects from :attr:`response_body_obj`.

        Returns:
            :obj:`dict`

        """
        obj = self.response_body_obj
        path = "soap:Envelope/soap:Body/t:return/result_object"
        src = "'result_object' element from SOAP API deserialized response body"
        data = self.get_dict_path(obj=obj, path=path, src=src)
        return data or {}

    def object_api(self, **kwargs):
        """Get :attr:`object_obj` deserialized into an ApiModel object.

        Args:
            **kwargs:
                rest of kwargs:
                    passed to :meth:`CommonMixin.obj_to_api`

        Returns:
            :obj:`pytan3.api_models.ApiModel`

        """
        if self.command_request in self.DATA_ROUTES:
            error = "Route {route!r} is not one of {data}, not a data request?"
            error = error.format(route=self.command_request, data=self.DATA_ROUTES)
            raise exceptions.ApiWrongRequestType(result=self, error=error)
        kwargs["src"] = "Result object from 'result_object' element in SOAP response"
        kwargs["api_name"] = list(self.object_obj.keys())[0]
        kwargs["obj"] = list(self.object_obj.values())[0]
        return self.obj_to_api(**kwargs)

    def str_to_obj(
        self, text, src, use_dict=True, try_int=True, flat_attrs=True, **kwargs
    ):
        """Deserialize string into a python object.

        Args:
            text (:obj:`str`):
                String to decode into python object
            src (:obj:`str`):
                Where text came from, used in error text.
            use_dict (:obj:`bool`):
                Use :obj:`dict` instead of :obj:`collections.OrderedDict` when
                deserializing.

                Defaults to: True.
            try_int (:obj:`bool`):
                Try to convert str into int when deserializing.

                Defaults to: True.
            flat_attrs (:obj:`bool`):
                Make attr_prefix "" and cdata_key "text".

                Defaults to: True.
            **kwargs:
                rest of kwargs:
                    Passed to xmltodict.parse.

        Raises:
            :exc:`exceptions.TextDeserializeError`:
                If an exception is thrown from xmltodict.parse.

        Returns:
            :obj:`dict`

        """
        if use_dict:
            kwargs.setdefault("dict_constructor", dict)
        if try_int:
            kwargs.setdefault("postprocessor", try_int_xml)
        if flat_attrs:
            kwargs.setdefault("attr_prefix", "")
            kwargs.setdefault("cdata_key", "text")

        with utils.tools.Timer() as t:
            if text:
                try:
                    ret = xmltodict.parse(text, **kwargs)
                except Exception as exc:
                    raise exceptions.TextDeserializeError(
                        result=self, text=text, src=src, exc=exc
                    )
            else:
                ret = {}
        size = utils.tools.human_size(size=len(text))
        m = "Finished deserializing {src} into {t}, {size} took {e}"
        m = m.format(size=size, src=src, t=type(ret), e=t.elapsed)
        self.log.debug(m)
        return ret


class Rest(CommonMixin, Result):
    """Deserialize REST API responses from Tanium API."""

    MANUAL_OBJECT_ROUTES = {
        "audit_logs": "audit_logs",
        # audit_logs needs to be an AuditLogList object
        # without this, it will be resolved to an AuditLog object
        "parse_question": "parse_question_results",
        # Use manual API object ParseQuestionResultList
    }
    """:obj:`dict`: Manual route defs for :meth:`object_api`."""

    DATA_ROUTES = {
        "result_info": "result_infos",
        "result_data": "result_sets",
        "merged_result_data": "merged_result_set",
    }
    """:obj:`dict`: Manual route defs for :meth:`data_api`."""

    def __call__(self, raw=False, **kwargs):
        """Get :attr:`data_api` or :attr:`object_api`.

        Args:
            raw (:obj:`bool`, optional):
                Return the serialized object instead of the object deserialized into
                an ApiModel.

                Defaults to: False.
            **kwargs:
                rest of kwargs:
                    passed to :meth:`object_api` or :meth:`data_api`.

        Notes:
            Will return :meth:`object_api` or :meth:`data_api` by
            determining if :attr:`RestUrlPath.route` is an object or data request.

        Returns:
            :obj:`pytan3.api_models.ApiModel` or :obj:`object`

        """
        self.error_check()
        is_result_data = self.url_path.route in self.DATA_ROUTES
        if is_result_data:
            _raw = self.data_obj
            _api = self.data_api
        else:
            _raw = self.object_obj
            _api = self.object_api
        return _raw if raw else _api(**kwargs)

    @property
    def error_map(self):
        """Map of status codes to regex patterns and exceptions.

        Notes:
            Keys should be :obj:`int` of a status code to check patterns of.

            Values should be :obj:`list` of [pattern, exc], where pattern is a regex
            pattern to search response body, and exc is exception to throw if pattern
            match is found.

        Raises:
            :exc:`exceptions.ObjectExistsError`
            :exc:`exceptions.ObjectNotFoundError`
            :exc:`exceptions.ResponseError`

        Returns:
            :obj:`dict`

        """
        ret = {}
        ret[400] = [
            [r"400.*already.*exists", exceptions.ObjectExistsError],
            [r"NotUnique", exceptions.ObjectExistsError],
        ]
        ret[404] = [[r".*", exceptions.ObjectNotFoundError]]
        return ret

    def error_check(self):
        """Check for errors in :attr:`CommonMixin.response_body_str`.

        Raises:
            :exc:`exceptions.ObjectExistsError`
            :exc:`exceptions.ObjectNotFoundError`
            :exc:`exceptions.ResponseError`

        """
        self.error_check_response()
        self.error_check_code()

    def error_check_response(self):
        """Check :attr:`CommonMixin.response_body_str` for errors.

        Notes:
            For each key value pair in :attr:`error_map`, if key matches
            :attr:`CommonMixin.status_code` or key is None, the patterns in value
            are checked against response body, and if matched the patterns associated
            exception is thrown.

        """
        for code, checks in self.error_map.items():
            if code is None or self.status_code == code:
                for check in checks:
                    pattern, error_exc = check
                    pattern_re = re.compile(pattern, re.IGNORECASE | re.DOTALL)
                    found = pattern_re.search(self.response_body_str)
                    if found:
                        raise error_exc(result=self, error=self.error_text)

    def error_check_code(self):
        """Check if :attr:`CommonMixin.status_code` is one of :attr:`valid_codes`.

        Raises:
            :exc:`exceptions.ResponseError`

        """
        if self.status_code not in self.valid_codes:
            error = "Response status code {c} is not one of {v}, error text:\n{e}"
            error = error.format(
                c=self.status_code, v=self.valid_codes, e=self.error_text
            )
            raise exceptions.ResponseError(result=self, error=error)

    @property
    def valid_codes(self):
        """List of valid status codes.

        Returns:
            :obj:`list` of :obj:`int`

        """
        return [200]

    @property
    def error_text(self):
        """Get the error text from :attr:`CommonMixin.response_body_str`.

        Returns:
            :obj:`str`

        """
        try:
            text = self.response_body_obj["text"]
            return ", ".join([x for x in text.splitlines() if x])
        except Exception:
            return self.response_body_obj

    @property
    def url_path(self):
        """Parse :attr:`CommonMixin.url` using :class:`RestUrlPath`.

        Returns:
            (:obj:`RestUrlPath`)

        """
        return RestUrlPath(url=self.url)

    @property
    def request_body_obj(self):
        """Deserialize :attr:`CommonMixin.request_body_str` into a python object.

        Returns:
            :obj:`dict`

        """
        key = "request_body_obj"
        if key not in self._cache:
            text = self.request_body_str or "{}"
            src = "REST API request body"
            self._cache[key] = self.str_to_obj(text=text, src=src)
        return self._cache[key]

    @property
    def request_object_obj(self):
        """Get the request objects from :attr:`request_body_obj`.

        Returns:
            :obj:`dict`

        """
        return self.request_body_obj

    @property
    def response_body_obj(self):
        """Get :attr:`CommonMixin.response_body_str` deserialized into a python object.

        Returns:
            :obj:`dict`

        """
        key = "response_body_obj"
        if key not in self._cache:
            text = self.response_body_str or "{}"
            src = "REST API response body"
            self._cache[key] = self.str_to_obj(text=text, src=src)
        return self._cache[key]

    @property
    def data_obj(self):
        """Get the response data from :attr:`response_body_obj`.

        Returns:
            :obj:`dict`

        """
        obj = self.response_body_obj
        path = "data"
        src = "'data' key from REST API deserialized response body"
        data = self.get_dict_path(obj=obj, path=path, src=src)
        return data or {}

    def data_api(self, **kwargs):
        """Get :attr:`data_obj` deserialized into an ApiModel object.

        Args:
            **kwargs:
                rest of kwargs:
                    passed to :meth:`CommonMixin.obj_to_api`

        Returns:
            :obj:`pytan3.api_models.ApiModel`

        """
        route = self.url_path.route
        if route not in self.DATA_ROUTES:
            error = "Route {route!r} is not one of {data}, not a data request?"
            error = error.format(route=route, data=self.DATA_ROUTES)
            raise exceptions.ApiWrongRequestType(result=self, error=error)
        override = self.DATA_ROUTES[route]
        cls = self.api_objects.cls_by_name(name=override)
        kwargs["src"] = "Result object from 'data' key in REST response"
        kwargs["api_name"] = cls.API_NAME
        kwargs["obj"] = self.data_obj
        return self.obj_to_api(**kwargs)

    @property
    def object_obj(self):
        """Get the response objects from :attr:`response_body_obj`.

        Returns:
            :obj:`dict`

        """
        obj = self.response_body_obj
        path = "data"
        src = "'data' key from REST API deserialized response body"
        data = self.get_dict_path(obj=obj, path=path, src=src)
        return data or {}

    def object_api(self, **kwargs):
        """Get :attr:`object_obj` deserialized into an ApiModel object.

        Args:
            **kwargs:
                rest of kwargs:
                    passed to :meth:`CommonMixin.obj_to_api`

        Returns:
            :obj:`pytan3.api_models.ApiModel`

        """
        """
        REST notes:
         - given path: /api/v2/actions
             - if GET and no target, returns `[{}, {}]` == ActionList()
             - if GET and target, returns `{}` == Action()
             - if POST, PATCH, DELETE, returns `{}` == Action()
         - given path: /api/v2/audit_logs
             - requires GET with target, returns
             `{"entries": [{}, {}]}` == AuditLogList()
         - action_stops has no GET without selector, so can't get all
        """
        route = self.url_path.route
        target = self.url_path.target
        if route in self.DATA_ROUTES:
            error = "Route {route!r} is one of {data}, not an object request?"
            error = error.format(route=route, data=self.DATA_ROUTES)
            raise exceptions.ApiWrongRequestType(result=self, error=error)

        if route in self.MANUAL_OBJECT_ROUTES:
            override = self.MANUAL_OBJECT_ROUTES[route]
            cls = self.api_objects.cls_by_name(name=override)
            kwargs["api_name"] = cls.API_NAME
        elif self.method == "GET" and target:
            # GET against target
            # a single item of type 'route' returned
            cls = self.api_objects.cls_by_name(name=route)
            kwargs["api_name"] = cls.API_ITEM_CLS.API_NAME
        elif self.method in ["POST", "PATCH", "DELETE"]:
            # POST/PATCH/DELETE
            # a single item of type 'route' returned
            cls = self.api_objects.cls_by_name(name=route)
            kwargs["api_name"] = cls.API_ITEM_CLS.API_NAME
        else:
            # no target and not POST/PATCH/DELETE
            # a list item type of 'route' returned
            cls = self.api_objects.cls_by_name(name=route)
            kwargs["api_name"] = cls.API_NAME

        src = "Result object from 'data' key in REST route {r}"
        src = src.format(r=route)
        kwargs["src"] = src
        kwargs["obj"] = self.object_obj
        return self.obj_to_api(**kwargs)

    def str_to_obj(self, text, src, **kwargs):
        """Deserialize string into a python object.

        Args:
            text (:obj:`str`):
                String to decode into python object
            src (:obj:`str`):
                Where text came from, used in error text.
            **kwargs:
                rest of kwargs:
                    Passed to :func:`json.loads`.

        Raises:
            :exc:`exceptions.TextDeserializeError`:
                If an exception is thrown from :func:`json.loads`.

        Returns:
            :obj:`object`

        """
        with utils.tools.Timer() as t:
            try:
                ret = json.loads(text, **kwargs)
            except Exception as exc:
                raise exceptions.TextDeserializeError(
                    result=self, text=text, src=src, exc=exc
                )

        size = utils.tools.human_size(size=len(text))
        m = "Finished deserializing {src} into {t}, {size} took {e}"
        m = m.format(size=size, src=src, t=type(ret), e=t.elapsed)
        self.log.debug(m)
        return ret


class RestUrlPath(object):
    """Parser to get path parts from a REST API URL."""

    def __init__(self, url):
        """Constructor.

        Args:
            url (:obj:`str`):
                URL to parse.

        Raises:
            :exc:`exceptions.ModuleError`:
                If :attr:`version` and :attr:`route` can not be parsed from
                :attr:`path_parts`.

        """
        self.url_original = url
        """:obj:`str`: Original URL supplied."""
        self.url = urllib.parse.unquote(url)
        """:obj:`str`: Percent decoded version of :attr:`url_original`."""
        self.url_path = urllib.parse.urlparse(self.url)
        """:obj:`urllib.parse.ParseResult`: Parsed version of :attr:`url`."""
        self.path_parts = self.url_path.path.lstrip("/").split("/")
        """:obj:`list` of :obj:`str`: Parts of URL split on /."""
        self.version = 0
        """:obj:`int`: REST API version from :attr:`path_parts`."""
        self.route = ""
        """:obj:`str`: REST API route from :attr:`path_parts`."""
        self.target = ""
        """:obj:`str`: If found, target supplied for :attr:`route` in :attr:`url`."""
        self.by_name = False
        """:obj:`bool`: If :attr:`target` is doing targeting by name or by id."""

        try:
            # first part should be "/api"
            self.path_parts.pop(0)
            # second part should be REST API version, ala "/v2"
            self.version = int(self.path_parts.pop(0).lstrip("v"))
            # third part should be route, ala "/users"
            self.route = self.path_parts.pop(0)
        except Exception as exc:
            error = "Failed to parse REST URL path as {p!r} from url {u!r}, error: {e}"
            error = error.format(u=self.url, e=exc, p="/api/v2/route")
            raise exceptions.ModuleError(error)

        self.by_name = any(x == "by-name" for x in self.path_parts)

        for idx, x in enumerate(self.path_parts[:]):
            if x == "by-name":
                value = self.path_parts.pop(idx + 1)
                self.path_parts.pop(idx)
                self.target = value
                break
            elif x.isdigit():
                self.target = self.path_parts.pop(idx)
                break

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        bits = [
            "version={!r}".format(self.version),
            "route={!r}".format(self.route),
            "target={!r}".format(self.target),
            "by-name={!r}".format(self.by_name),
            "leftover_parts={!r}".format(self.path_parts),
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


def try_int_xml(path, key, value):
    """Parser hook for xmltodict.parse to try to convert str to int.

    Args:
        path (:obj:`list`):
            Path from root of document to key.
        key (:obj:`str`):
            Element name being parsed.
        value (:obj:`object`):
            Element value of key being parsed.

    Returns:
        (:obj:`str`, :obj:`object`):
            original key supplied and value as int if successfully converted.

    """
    if isinstance(value, six.string_types):
        try:
            return key, int(value)
        except (ValueError, TypeError):
            return key, value
    return key, value

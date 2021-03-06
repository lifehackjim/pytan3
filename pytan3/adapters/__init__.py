# -*- coding: utf-8 -*-
"""Adapter objects that serialize requests to the Tanium API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import abc
import json
import re
import six
import warnings
import xmltodict

from . import exceptions
from .. import api_models
from .. import results
from .. import utils

DEFAULT_NAME = "soap"
""":obj:`str`: Default :class:`Adapter` name to load in :func:`load`."""

DEFAULT_TYPE = "soap"
""":obj:`str`: Default :class:`Adapter` type to load in :func:`load_type`."""


@six.add_metaclass(abc.ABCMeta)
class Adapter(object):
    """Abstract base class for all Adapters."""

    @abc.abstractproperty
    def api_objects(self):
        """Get the API objects container.

        Returns:
            :obj:`pytan3.api_objects.ApiObjects`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def api_client(self):
        """Get the API client.

        Returns:
            :obj:`pytan3.api_clients.ApiClient`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def http_client(self):
        """Get the HTTP client.

        Returns:
            :obj:`pytan3.http_client.HttpClient`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def auth_method(self):
        """Get the Auth Method.

        Returns:
            :obj:`pytan3.auth_methods.AuthMethod`

        """
        raise NotImplementedError  # pragma: no cover

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
    def result_cls(cls):
        """Get the result deserializer class.

        Returns:
            :class:`pytan3.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def api_get(self, obj, **kwargs):
        """Send an API request to get an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.

        Returns:
            :obj:`pytan3.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def api_add(self, obj, **kwargs):
        """Send an API request to add an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.

        Returns:
            :obj:`pytan3.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def api_delete(self, obj, **kwargs):
        """Send an API request to delete an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.

        Returns:
            :obj:`pytan3.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def api_update(self, obj, **kwargs):
        """Send an API request to update an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.

        Returns:
            :obj:`pytan3.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def api_get_audit_logs(self, type, target, **kwargs):
        """Send an API request to get audit logs for an object.

        Args:
            type (:obj:`str`):
                Type of object to get audit logs of.
            target (:obj:`int`):
                ID of object type to get audit logs for.

        Returns:
            :obj:`pytan3.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def api_get_client_count(self, **kwargs):
        """Send an API request to get the client count.

        Returns:
            :obj:`pytan3.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def api_parse_question(self, text, **kwargs):
        """Send an API request to parse text.

        Args:
            text (:obj:`str`):
                Text to parse into question objects.

        Returns:
            :obj:`pytan3.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def api_add_parsed_question(self, obj, **kwargs):
        """Send an API request to add a parsed question object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.

        Returns:
            :obj:`pytan3.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def api_get_result_info(self, obj, **kwargs):
        """Send an API request to get result info for an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.

        Returns:
            :obj:`pytan3.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def api_get_result_data(self, obj, **kwargs):
        """Send an API request to get result data for an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.

        Returns:
            :obj:`pytan3.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def api_get_merged_result_data(self, objlist, **kwargs):
        """Send an API request to get merged result data for a list of objects.

        Args:
            objlist (:obj:`list`):
                List of API Objects to use for request.

        Returns:
            :obj:`pytan3.results.Result`

        """
        raise NotImplementedError  # pragma: no cover


class Soap(Adapter):
    """Tanium SOAP request adapter."""

    DEFAULT_OPTIONS = {"json_pretty_print": True, "include_hashes_flag": True}
    """:obj:`dict`: Default options to use in :meth:`build_options_from_kwargs`."""

    AUDIT_LOG_TYPES = [
        "authentication",
        "content_set",
        "content_set_role",
        "content_set_role_privilege",
        "dashboard",
        "dashboard_group",
        "group",
        "package_spec",
        "plugin_schedule",
        "saved_action",
        "saved_question",
        "sensor",
        "system_setting",
        "user",
        "user_group",
        "white_listed_url",
    ]
    """:obj:`list` of :obj:`str`: Valid types for :meth:`api_get_audit_logs`."""

    def __init__(self, api_client, api_objects, ver_check=True, lvl="info"):
        """Constructor.

        Args:
            api_client (:obj:`pytan3.api_clients.ApiClient`):
                Client to use for sending API requests.
            api_objects (:obj:`pytan3.api_objects.ApiObjects`):
                API objects container to use for this adapter.
            ver_check (:obj:`bool`, optional):
                Perform version checks against :func:`pytan3.api_clients.get_version`.

                Defaults to: True.
            lvl (:obj:`str`, optional):
                Logging level.

                Defaults to: "info".

        """
        self.log = utils.logs.get_obj_log(obj=self, lvl=lvl)
        """:obj:`logging.Logger`: Log."""

        self._api_objects = api_objects
        self._api_client = api_client
        check_adapter_types(self)
        if ver_check and any(self.get_version_req().values()):
            check_adapter_version(self)

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        bits = [
            "type={!r}".format(self.get_type()),
            "api_objects={!r}".format(self.api_objects),
            "api_client={!r}".format(self.api_client),
            "http_client={!r}".format(self.http_client),
            "auth_method={!r}".format(self.auth_method),
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

    @property
    def api_objects(self):
        """Get the API objects container.

        Returns:
            :obj:`pytan3.api_objects.ApiObjects`

        """
        return self._api_objects

    @property
    def api_client(self):
        """Get the API client.

        Returns:
            :obj:`pytan3.api_clients.ApiClient`

        """
        return self._api_client

    @property
    def http_client(self):
        """Get the HTTP client.

        Returns:
            :obj:`pytan3.http_client.HttpClient`

        """
        return self.api_client.http_client

    @property
    def auth_method(self):
        """Get the Auth Method.

        Returns:
            :obj:`pytan3.auth_methods.AuthMethod`

        """
        return self.api_client.auth_method

    @classmethod
    def get_name(cls):
        """Get the ref name of this class for use by :func:`load`.

        Returns:
            :obj:`str`

        """
        return "soap"

    @classmethod
    def get_type(cls):
        """Get the ref type of this class for use by :func:`load_type`.

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
    def result_cls(cls):
        """Get the result deserializer class.

        Returns:
            :class:`pytan3.results.Result`

        """
        return results.Soap

    def build_options_from_kwargs(self, **kwargs):
        """Build an Options API object from kwargs and return the serialized form.

        Args:
            **kwargs:
                options_obj (:obj:`pytan3.api_models.ApiItem`):
                    A pre-established Options object.

                    Defaults to: new Options object from :attr:`api_objects`.
                rest of kwargs:
                    Set on Options object if key is an attr on object and attrs value
                    is None.

        Notes:
            Will set :attr:`DEFAULT_OPTIONS` as defaults to kwargs
            before applying values to Options object attributes.

        Returns:
            :obj:`dict`

        """
        default_options = getattr(self, "DEFAULT_OPTIONS", {}) or {}
        for k, v in default_options.items():
            kwargs.setdefault(k, v)
        opts = kwargs.pop("options_obj", self.api_objects.Options())
        check_object_type(obj=opts, types=(self.api_objects.Options,))
        for k in list(kwargs):
            if hasattr(opts, k) and getattr(opts, k, None) is None:
                setattr(opts, k, kwargs[k])
        return opts.serialize(wrap_name=False)

    def send(self, obj, cmd, **kwargs):
        """Build and send a SOAP API request.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                ApiModel to serialize and send as part of request.
            cmd (:obj:`str`):
                SOAP Command to use in request.
            **kwargs:
                body_re_limit (:obj:`int`):
                    Value to limit regex search of response body for <session> tag.

                    Defaults to: 4000.
                empty (:obj:`bool`):
                    Include attributes that have a value of None when serializing.

                    Defaults to: False
                list_attrs (:obj:`bool`):
                    Include simple attributes of :obj:`pytan3.api_models.ApiList`
                    when serializing.

                    Defaults to: False.
                exclude_attrs (:obj:`list` of :obj:`str`):
                    Exclude these attributes when serializing.

                    Defaults to: [].
                only_attrs (:obj:`list` of :obj:`str`):
                    Include only these attributes when serializing.

                    Defaults to: [].
                wrap_name (:obj:`bool`):
                    Wrap the return in another dict whose key is set to the API name.

                    Defaults to: True.
                wrap_item_attr (:obj:`bool`):
                    Wrap list items in dict whose key is set to the API list
                    item attribute.

                    Defaults to: True.
                rest of kwargs:
                    Passed to :meth:`build_options_from_kwargs`.

        Raises:
            :obj:`exceptions.SessionNotFoundWarning`:
                If the <session> tag can not be found in the response body.

        Returns:
            :obj:`pytan3.results.Result`

        """
        limit = kwargs.pop("body_re_limit", 4000)
        sargs = {
            "only_attrs": kwargs.pop("only_attrs", []),
            "exclude_attrs": kwargs.pop("exclude_attrs", []),
            "empty": kwargs.pop("empty", False),
            "list_attrs": kwargs.pop("list_attrs", False),
            "wrap_name": kwargs.pop("wrap_name", True),
            "wrap_item_attr": kwargs.pop("wrap_item_attr", True),
        }

        obj = obj.serialize(**sargs) if isinstance(obj, api_models.ApiModel) else obj
        opts = self.build_options_from_kwargs(**kwargs)

        request_dict = soap_envelope(cmd=cmd, obj=obj, opts=opts)
        request_body = serialize_xml(obj=request_dict)
        response = self.api_client(data=request_body)

        try:
            auth_token = re_soap_tag(text=response.text, tag="session", limit=limit)
        except Exception:
            auth_token = ""

        if auth_token:
            self.api_client.auth_method.token = auth_token
        else:
            error = "XML tag 'session' not in {limit} characters of SOAP response body"
            error = error.format(limit="the first {}".format(limit) or "ALL")
            warnings.warn(error, exceptions.SessionNotFoundWarning)
        return self.result_cls.from_response(
            api_objects=self.api_objects, response=response, lvl=self.log.level
        )

    def api_get(self, obj, **kwargs):
        """Send an API request to get an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        check_object_type(
            obj=obj, types=(self.api_objects.ApiItem, self.api_objects.ApiList)
        )
        kwargs["cmd"] = "GetObject"
        return self.send(obj=obj, **kwargs)

    def api_add(self, obj, **kwargs):
        """Send an API request to add an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        check_object_type(obj=obj, types=(self.api_objects.ApiItem,))
        kwargs["cmd"] = "AddObject"
        kwargs["exclude_attrs"] = ["id"]
        return self.send(obj=obj, **kwargs)

    def api_delete(self, obj, **kwargs):
        """Send an API request to delete an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        check_object_type(obj=obj, types=(self.api_objects.ApiItem,))
        check_object_attrs(obj=obj, attrs=["id", "name"])
        kwargs["cmd"] = "DeleteObject"
        return self.send(obj=obj, **kwargs)

    def api_update(self, obj, **kwargs):
        """Send an API request to update an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        check_object_type(obj=obj, types=(self.api_objects.ApiItem,))
        check_object_attrs(obj=obj, attrs=["id", "name"])
        kwargs["cmd"] = "UpdateObject"
        return self.send(obj=obj, **kwargs)

    def api_get_audit_logs(self, type, target, **kwargs):
        """Send an API request to get audit logs for an object.

        Args:
            type (:obj:`str`):
                Type of object to get audit logs of.
            target (:obj:`int`):
                ID of object type to get audit logs for.
                SOAP allows target of 'None' to get all objects of `type`.
            **kwargs:
                count (:obj:`int`):
                    Limit number of audit logs returned to this.

                    Defaults to: 1.
                rest of kwargs:
                    Passed to :meth:`send`.

        Raises:
            :exc:`exceptions.InvalidTypeError`:
                If type is not one of :attr:`AUDIT_LOG_TYPES`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        if type not in self.AUDIT_LOG_TYPES:
            error = "Invalid object type {ot} - MUST be one of {at}"
            error = error.format(at=self.AUDIT_LOG_TYPES, ot=type)
            raise exceptions.InvalidTypeError(error)

        obj = self.api_objects.AuditLog(type="{t}_audit".format(t=type), id=target)
        kwargs.setdefault("audit_history_size", kwargs.pop("count", 1))
        kwargs["cmd"] = "GetObject"
        return self.send(obj=obj, **kwargs)

    def api_get_client_count(self, **kwargs):
        """Send an API request to get the client count.

        Args:
            **kwargs:
                count (:obj:`int`):
                    Number of days to get client count for.

                    Defaults to: 30.
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        obj = {"client_count": kwargs.pop("count", 30)}
        kwargs["cmd"] = "GetObject"
        return self.send(obj=obj, **kwargs)

    def api_parse_question(self, text, **kwargs):
        """Send an API request to parse text.

        Args:
            text (:obj:`str`):
                Text to parse into question objects.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        check_object_type(obj=text, types=six.string_types)
        obj = self.api_objects.ParseJob(question_text=text)
        kwargs["cmd"] = "AddObject"
        return self.send(obj=obj, **kwargs)

    def api_add_parsed_question(self, obj, **kwargs):
        """Send an API request to add a parsed question object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                for_merge (:obj:`bool`):
                    Value for force_computer_id_flag attr on question object.

                    Defaults to: True.
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        check_object_type(obj=obj, types=(self.api_objects.ParseResultGroup,))
        obj = obj.question
        obj.force_computer_id_flag = int(kwargs.pop("for_merge", True))
        kwargs["cmd"] = "AddObject"
        return self.send(obj=obj, **kwargs)

    def api_get_result_info(self, obj, **kwargs):
        """Send an API request to get result info for an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        types = (
            self.api_objects.Question,
            self.api_objects.SavedQuestion,
            self.api_objects.Action,
            self.api_objects.SavedAction,
        )
        check_object_type(obj=obj, types=types)
        check_object_attrs(obj=obj, attrs=["id", "name"])
        kwargs["cmd"] = "GetResultInfo"
        kwargs["only_attrs"] = ["id", "name"]
        return self.send(obj=obj, **kwargs)

    def api_get_result_data(self, obj, **kwargs):
        """Send an API request to get result data for an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        types = (
            self.api_objects.Question,
            self.api_objects.SavedQuestion,
            self.api_objects.Action,
            self.api_objects.SavedAction,
        )
        check_object_type(obj=obj, types=types)
        check_object_attrs(obj=obj, attrs=["id", "name"])
        kwargs["cmd"] = "GetResultData"
        kwargs["only_attrs"] = ["id", "name"]
        return self.send(obj=obj, **kwargs)

    def api_get_merged_result_data(self, objlist, **kwargs):
        """Send an API request to get merged result data for a list of objects.

        Args:
            objlist (:obj:`list`):
                List of API Objects to use for request.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        list_types = (
            list,
            tuple,
            self.api_objects.SavedQuestionList,
            self.api_objects.QuestionList,
        )
        check_object_type(obj=objlist, types=list_types)

        item_types = (self.api_objects.Question, self.api_objects.SavedQuestion)
        pobjlist = [objlist] if isinstance(objlist, item_types) else objlist

        objs = {"question": [], "saved_question": []}
        only_attrs = ["id", "name", "index", "cache_row_id"]
        sargs = {"wrap_name": False, "wrap_item_attr": False, "only_attrs": only_attrs}
        idx = 0
        for pobj in pobjlist:
            sobjlist = [pobj] if isinstance(pobj, item_types) else pobj
            for sobj in sobjlist:
                check_object_type(obj=sobj, types=item_types)
                check_object_attrs(obj=sobj, attrs=["id", "name"])
                sobj.index = idx
                sobj.cache_row_id = getattr(sobj, "cache_row_id", None) or 0
                sobj_dict = sobj.serialize(**sargs)
                objs_target = sobj.API_NAME
                objs[objs_target].append(sobj_dict)
                idx += 1

        kwargs["cmd"] = "GetMergedResultData"
        return self.send(obj=objs, **kwargs)


class Rest(Adapter):
    """Tanium REST API request adapter."""

    DEFAULT_OPTIONS = {"json_pretty_print": True, "include_hashes_flag": True}
    """:obj:`dict`: Default options to use in :meth:`build_options_from_kwargs`."""

    AUDIT_LOG_TYPES = [  # REST routes all need to be pluralized
        "content_set",
        "content_set_role",
        "dashboard",
        "dashboard_group",
        "group",
        "package",  # REST docs say "package_spec", but only "packages" route works
        "plugin_schedule",
        "saved_action",
        "saved_question",
        "sensor",
        "system_setting",
        "user",
        "user_group",
        "white_listed_url",
    ]
    """:obj:`list` of :obj:`str`: Valid types for :meth:`api_get_audit_logs`."""

    def __init__(self, api_client, api_objects, ver_check=True, lvl="info"):
        """Constructor.

        Args:
            api_client (:obj:`pytan3.api_clients.ApiClient`):
                Client to use for sending API requests.
            api_objects (:obj:`pytan3.api_objects.ApiObjects`):
                API objects container to use for this adapter.
            ver_check (:obj:`bool`, optional):
                Perform version checks against :func:`pytan3.api_clients.get_version`.

                Defaults to: True.
            lvl (:obj:`str`, optional):
                Logging level.

                Defaults to: "info".

        """
        self.log = utils.logs.get_obj_log(obj=self, lvl=lvl)
        """:obj:`logging.Logger`: Log."""

        self._api_objects = api_objects
        self._api_client = api_client
        check_adapter_types(self)
        if ver_check and any(self.get_version_req().values()):
            check_adapter_version(self)

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        bits = [
            "type={!r}".format(self.get_type()),
            "api_objects={!r}".format(self.api_objects),
            "api_client={!r}".format(self.api_client),
            "http_client={!r}".format(self.http_client),
            "auth_method={!r}".format(self.auth_method),
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

    @property
    def api_objects(self):
        """Get the API objects container.

        Returns:
            :obj:`pytan3.api_objects.ApiObjects`

        """
        return self._api_objects

    @property
    def api_client(self):
        """Get the API client.

        Returns:
            :obj:`pytan3.api_clients.ApiClient`

        """
        return self._api_client

    @property
    def http_client(self):
        """Get the HTTP client.

        Returns:
            :obj:`pytan3.http_client.HttpClient`

        """
        return self.api_client.http_client

    @property
    def auth_method(self):
        """Get the Auth Method.

        Returns:
            :obj:`pytan3.auth_methods.AuthMethod`

        """
        return self.api_client.auth_method

    @classmethod
    def get_name(cls):
        """Get the ref name of this class for use by :func:`load`.

        Returns:
            :obj:`str`

        """
        return "rest"

    @classmethod
    def get_type(cls):
        """Get the ref type of this class for use by :func:`load_type`.

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
    def result_cls(cls):
        """Get the result deserializer class.

        Returns:
            :class:`pytan3.results.Result`

        """
        return results.Rest

    def build_options_from_kwargs(self, **kwargs):
        """Build an Options API object from kwargs and return the serialized form.

        Args:
            **kwargs:
                options_obj (:obj:`pytan3.api_models.ApiItem`):
                    A pre-established Options object.

                    Defaults to: new Options object from :attr:`api_objects`.
                rest of kwargs:
                    Set on Options object if key is an attr on object and attrs value
                    is None.

        Notes:
            Will set :attr:`DEFAULT_OPTIONS` as defaults to kwargs
            before applying values to Options object attributes.

        Returns:
            :obj:`dict`

        """
        default_options = getattr(self, "DEFAULT_OPTIONS", {}) or {}
        for k, v in default_options.items():
            kwargs.setdefault(k, v)
        opts = kwargs.pop("options_obj", self.api_objects.Options())
        check_object_type(obj=opts, types=(self.api_objects.Options,))
        for k in list(kwargs):
            if hasattr(opts, k) and getattr(opts, k, None) is None:
                setattr(opts, k, kwargs[k])
        return opts.serialize(wrap_name=False)

    def api_get(self, obj, **kwargs):
        """Send an API request to get an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                headers (:obj:`dict`):
                    Headers to supply to request.

                    Defaults to: {}.
                params (:obj:`dict`):
                    Parameters to supply to request.

                    Defaults to: {}.
                rest of kwargs:
                    Passed to :meth:`build_options_from_kwargs`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        check_object_type(
            obj=obj, types=(self.api_objects.ApiItem, self.api_objects.ApiList)
        )
        check_object_attrs(obj=obj, attrs=["id", "name"])

        headers = kwargs.pop("headers", {})
        params = kwargs.pop("params", {})

        opts = self.build_options_from_kwargs(**kwargs)
        headers.setdefault("tanium-options", serialize_json(obj=opts, indent=None))

        response = self.api_client(
            method="get",
            endpoint=magic_endpoint(obj=obj, auto_target=True, needs_target=False),
            params=params,
            headers=headers,
        )
        return self.result_cls.from_response(
            api_objects=self.api_objects, response=response, lvl=self.log.level
        )

    def api_add(self, obj, **kwargs):
        """Send an API request to add an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                headers (:obj:`dict`):
                    Headers to supply to request.

                    Defaults to: {}.
                params (:obj:`dict`):
                    Parameters to supply to request.

                    Defaults to: {}.
                rest of kwargs:
                    Passed to :meth:`build_options_from_kwargs`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        check_object_type(obj=obj, types=(self.api_objects.ApiItem,))

        headers = kwargs.pop("headers", {})
        params = kwargs.pop("params", {})

        opts = self.build_options_from_kwargs(**kwargs)
        headers.setdefault("tanium-options", serialize_json(obj=opts, indent=None))

        obj_dict = obj.serialize(
            exclude_attrs=["id"], wrap_name=False, wrap_item_attr=False
        )

        response = self.api_client(
            method="post",
            data=serialize_json(obj=obj_dict),
            endpoint=magic_endpoint(obj=obj, auto_target=False, needs_target=False),
            params=params,
            headers=headers,
        )
        return self.result_cls.from_response(
            api_objects=self.api_objects, response=response, lvl=self.log.level
        )

    def api_delete(self, obj, **kwargs):
        """Send an API request to delete an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                headers (:obj:`dict`):
                    Headers to supply to request.

                    Defaults to: {}.
                params (:obj:`dict`):
                    Parameters to supply to request.

                    Defaults to: {}.
                rest of kwargs:
                    Passed to :meth:`build_options_from_kwargs`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        check_object_type(obj=obj, types=(self.api_objects.ApiItem,))
        check_object_attrs(obj=obj, attrs=["id"])

        headers = kwargs.pop("headers", {})
        params = kwargs.pop("params", {})

        opts = self.build_options_from_kwargs(**kwargs)
        headers.setdefault("tanium-options", serialize_json(obj=opts, indent=None))

        response = self.api_client(
            method="delete",
            endpoint=magic_endpoint(obj=obj, auto_target=True, needs_target=True),
            params=params,
            headers=headers,
        )
        return self.result_cls.from_response(
            api_objects=self.api_objects, response=response, lvl=self.log.level
        )

    def api_update(self, obj, **kwargs):
        """Send an API request to update an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                headers (:obj:`dict`):
                    Headers to supply to request.

                    Defaults to: {}.
                params (:obj:`dict`):
                    Parameters to supply to request.

                    Defaults to: {}.
                rest of kwargs:
                    Passed to :meth:`build_options_from_kwargs`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        check_object_type(obj=obj, types=(self.api_objects.ApiItem,))
        check_object_attrs(obj=obj, attrs=["id", "name"])

        headers = kwargs.pop("headers", {})
        params = kwargs.pop("params", {})

        opts = self.build_options_from_kwargs(**kwargs)
        headers.setdefault("tanium-options", serialize_json(obj=opts, indent=None))

        # LATER(!) no id if id in target, but no name if name in target, rite?
        obj_dict = obj.serialize(
            exclude_attrs=["name", "id"], wrap_name=False, wrap_item_attr=False
        )

        response = self.api_client(
            method="patch",
            data=serialize_json(obj=obj_dict),
            endpoint=magic_endpoint(obj=obj, auto_target=True, needs_target=True),
            params=params,
            headers=headers,
        )
        return self.result_cls.from_response(
            api_objects=self.api_objects, response=response, lvl=self.log.level
        )

    def api_get_audit_logs(self, type, target, **kwargs):
        """Send an API request to get audit logs for an object.

        Args:
            type (:obj:`str`):
                Type of object to get audit logs of.
            target (:obj:`int`):
                ID of object type to get audit logs for.
            **kwargs:
                count (:obj:`int`):
                    Limit number of audit logs returned to this.

                    Defaults to: 1.
                headers (:obj:`dict`):
                    Headers to supply to request.

                    Defaults to: {}.
                params (:obj:`dict`):
                    Parameters to supply to request.

                    Defaults to: {}.
                rest of kwargs:
                    Passed to :meth:`build_options_from_kwargs`.

        Raises:
            :exc:`exceptions.InvalidTypeError`:
                If type is not one of :attr:`AUDIT_LOG_TYPES`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        if type not in self.AUDIT_LOG_TYPES:
            error = "Invalid object type {ot} - MUST be one of {at}"
            error = error.format(at=self.AUDIT_LOG_TYPES, ot=type)
            raise exceptions.InvalidTypeError(error)

        headers = kwargs.pop("headers", {})
        params = kwargs.pop("params", {})

        kwargs.setdefault("audit_history_size", kwargs.pop("count", 1))
        opts = self.build_options_from_kwargs(**kwargs)
        headers.setdefault("tanium-options", serialize_json(obj=opts, indent=None))

        route = "audit_logs/{type}s".format(type=type)

        response = self.api_client(
            method="get",
            endpoint=build_endpoint(route=route, target=target),
            params=params,
            headers=headers,
        )
        return self.result_cls.from_response(
            api_objects=self.api_objects, response=response, lvl=self.log.level
        )

    def api_parse_question(self, text, **kwargs):
        """Send an API request to parse text.

        Args:
            text (:obj:`str`):
                Text to parse into question objects.
            **kwargs:
                headers (:obj:`dict`):
                    Headers to supply to request.

                    Defaults to: {}.
                params (:obj:`dict`):
                    Parameters to supply to request.

                    Defaults to: {}.
                rest of kwargs:
                    Passed to :meth:`build_options_from_kwargs`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        check_object_type(obj=text, types=(six.string_types,))

        headers = kwargs.pop("headers", {})
        params = kwargs.pop("params", {})

        opts = self.build_options_from_kwargs(**kwargs)
        headers.setdefault("tanium-options", serialize_json(obj=opts, indent=None))

        obj_dict = {"text": text}
        route = "parse_question"

        response = self.api_client(
            method="post",
            data=serialize_json(obj=obj_dict),
            endpoint=build_endpoint(route=route),
            params=params,
            headers=headers,
        )
        return self.result_cls.from_response(
            api_objects=self.api_objects, response=response, lvl=self.log.level
        )

    def api_get_client_count(self, **kwargs):
        """Send an API request to get the client count.

        Args:
            **kwargs:
                headers (:obj:`dict`):
                    Headers to supply to request.

                    Defaults to: {}.
                params (:obj:`dict`):
                    Parameters to supply to request.

                    Defaults to: {}.
                rest of kwargs:
                    Passed to :meth:`build_options_from_kwargs`.

        Notes:
            Unlike the SOAP API, "count" does not seem to be used by REST API.

        Returns:
            :obj:`pytan3.results.Result`

        """
        headers = kwargs.pop("headers", {})
        params = kwargs.pop("params", {})

        opts = self.build_options_from_kwargs(**kwargs)
        headers.setdefault("tanium-options", serialize_json(obj=opts, indent=None))

        route = "client_count"

        response = self.api_client(
            method="get",
            endpoint=build_endpoint(route=route),
            params=params,
            headers=headers,
        )
        return self.result_cls.from_response(
            api_objects=self.api_objects, response=response, lvl=self.log.level
        )

    def api_add_parsed_question(self, obj, **kwargs):
        """Send an API request to add a parsed question object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                for_merge (:obj:`bool`):
                    Set option "force_computer_id_flag".

                    Defaults to: True.
                headers (:obj:`dict`):
                    Headers to supply to request.

                    Defaults to: {}.
                params (:obj:`dict`):
                    Parameters to supply to request.

                    Defaults to: {}.
                rest of kwargs:
                    Passed to :meth:`build_options_from_kwargs`.


        Returns:
            :obj:`pytan3.results.Result`

        """
        check_object_type(obj=obj, types=(self.api_objects.ParseQuestionResult,))

        headers = kwargs.pop("headers", {})
        params = kwargs.pop("params", {})

        obj.force_computer_id_flag = int(kwargs.pop("for_merge", True))

        opts = self.build_options_from_kwargs(**kwargs)
        headers.setdefault("tanium-options", serialize_json(obj=opts, indent=None))

        obj_dict = obj.serialize(
            exclude_attrs=["id"], wrap_name=False, wrap_item_attr=False
        )

        route = "questions"

        response = self.api_client(
            method="post",
            data=serialize_json(obj=obj_dict),
            endpoint=build_endpoint(route=route),
            params=params,
            headers=headers,
        )
        return self.result_cls.from_response(
            api_objects=self.api_objects, response=response, lvl=self.log.level
        )

    def api_get_result_info(self, obj, **kwargs):
        """Send an API request to get result info for an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                headers (:obj:`dict`):
                    Headers to supply to request.

                    Defaults to: {}.
                params (:obj:`dict`):
                    Parameters to supply to request.

                    Defaults to: {}.
                rest of kwargs:
                    Passed to :meth:`build_options_from_kwargs`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        # LATER(!) Action and SavedAction not in REST docs!
        types = (self.api_objects.Question, self.api_objects.SavedQuestion)
        check_object_type(obj=obj, types=types)
        check_object_attrs(obj=obj, attrs=["id"])

        headers = kwargs.pop("headers", {})
        params = kwargs.pop("params", {})

        opts = self.build_options_from_kwargs(**kwargs)
        headers.setdefault("tanium-options", serialize_json(obj=opts, indent=None))

        route = "result_info/{}".format(obj.API_NAME)

        response = self.api_client(
            method="get",
            endpoint=build_endpoint(route=route, target=obj.id),
            params=params,
            headers=headers,
        )
        return self.result_cls.from_response(
            api_objects=self.api_objects, response=response, lvl=self.log.level
        )

    def api_get_result_data(self, obj, **kwargs):
        """Send an API request to get result data for an object.

        Args:
            obj (:obj:`pytan3.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                headers (:obj:`dict`):
                    Headers to supply to request.

                    Defaults to: {}.
                params (:obj:`dict`):
                    Parameters to supply to request.

                    Defaults to: {}.
                rest of kwargs:
                    Passed to :meth:`build_options_from_kwargs`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        # LATER(!) Action and SavedAction not in REST docs!
        types = (self.api_objects.Question, self.api_objects.SavedQuestion)
        check_object_type(obj=obj, types=types)
        check_object_attrs(obj=obj, attrs=["id"])

        headers = kwargs.pop("headers", {})
        params = kwargs.pop("params", {})

        opts = self.build_options_from_kwargs(**kwargs)
        headers.setdefault("tanium-options", serialize_json(obj=opts, indent=None))

        route = "result_data/{}".format(obj.API_NAME)

        response = self.api_client(
            method="get",
            endpoint=build_endpoint(route=route, target=obj.id),
            params=params,
            headers=headers,
        )
        return self.result_cls.from_response(
            api_objects=self.api_objects, response=response, lvl=self.log.level
        )

    def api_get_merged_result_data(self, objlist, **kwargs):
        """Send an API request to get merged result data for a list of objects.

        Args:
            objlist (:obj:`list`):
                List of API Objects to use for request.
            **kwargs:
                headers (:obj:`dict`):
                    Headers to supply to request.

                    Defaults to: {}.
                params (:obj:`dict`):
                    Parameters to supply to request.

                    Defaults to: {}.
                rest of kwargs:
                    Passed to :meth:`build_options_from_kwargs`.

        Returns:
            :obj:`pytan3.results.Result`

        """
        list_types = (
            list,
            tuple,
            self.api_objects.SavedQuestionList,
            self.api_objects.QuestionList,
        )
        check_object_type(obj=objlist, types=list_types)

        item_types = (self.api_objects.Question, self.api_objects.SavedQuestion)
        pobjlist = [objlist] if isinstance(objlist, item_types) else objlist

        targets = []
        for pobj in pobjlist:
            sobjlist = [pobj] if isinstance(pobj, item_types) else pobj
            for sobj in sobjlist:
                check_object_type(obj=sobj, types=item_types)
                check_object_attrs(obj=sobj, attrs=["id"])
                targets.append("{}/{}".format(sobj.API_NAME, sobj.id))

        headers = kwargs.pop("headers", {})
        params = kwargs.pop("params", {})

        opts = self.build_options_from_kwargs(**kwargs)
        headers.setdefault("tanium-options", serialize_json(obj=opts, indent=None))

        target = "/".join(targets)
        route = "merged_result_data"

        response = self.api_client(
            method="get",
            endpoint=build_endpoint(route=route, target=target),
            params=params,
            headers=headers,
        )
        return self.result_cls.from_response(
            api_objects=self.api_objects, response=response, lvl=self.log.level
        )


def soap_envelope(cmd, obj, opts=None):
    """Construct a SOAP envelope with the request command, obj, and options.

    Args:
        cmd (:obj:`str`):
            Command to use for request.
        obj (:obj:`dict`):
            Object(s) to use for request.
        options (:obj:`dict`, optional):
            Options to use for request.

            Defaults to: None.

    Returns:
        :obj:`dict`

    """
    request = {"command": cmd, "object_list": obj, "options": opts}

    body = {
        "@xmlns:t": "urn:TaniumSOAP",
        "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "t:tanium_soap_request": request,
    }
    env = {
        "@soap:encodingStyle": "http://schemas.xmlsoap.org/soap/encoding/",
        "@xmlns:soap": "http://schemas.xmlsoap.org/soap/envelope/",
        "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
        "soap:Body": body,
    }
    ret = {"soap:Envelope": env}
    return ret


def re_soap_tag(text, tag, limit=4000, pattern=r"<{t}>(.*?)</{t}>"):
    """Search for tag in text[:limit] using pattern.

    Args:
        text (:obj:`str`):
            Text to search for pattern.
        tag (:obj:`str`):
            Tag name to use in pattern as 't'.
        limit (:obj:`int`, optional):
            Length to limit text to when searching for pattern.

            Defaults to: 4000.
        pattern (:obj:`str`, optional):
            Pattern to use when searching for tag.

            Defaults to: r'<{e}>(.*?)</{e}>'

    Notes:
        Given text is 4 GB and pattern is expected at top of text:
            * if head is None and pattern not found: 131 seconds
            * if head is None and pattern found: 0 seconds
            * if head is 4000 and pattern not found: 0 seconds
            * if head is 4000 and pattern found: 0 seconds

    Returns:
        :obj:`str`

    """
    pattern_txt = pattern.format(t=tag)
    pattern_re = re.compile(pattern_txt, re.IGNORECASE | re.DOTALL)
    text_limit = text[:limit]
    match = pattern_re.search(text_limit)
    return match.group(1) if match else ""


def magic_endpoint(obj, target=None, auto_target=True, needs_target=False):
    """Build a REST API endpoint from an API object.

    Args:
        obj (:obj:`pytan3.api_models.ApiModel`):
            API object to get route and target from in order to build endpoint.
        target (:obj:`str`, optional):
            Manually provided target.

            Defaults to: None.
        auto_target (:obj:`bool`, optional):
            Try to identify the target from obj by getting "id" or "name" attributes
            if their values are not None.

            Defaults to: True.
        needs_target (:obj:`bool`, optional):
            Throw an exception if a target is not automatically determined from obj.

            Defaults to: False.

    Raises:
        :exc:`exceptions.ModuleError`:
            If needs_target is True and resolved target is None.

    Returns:
        :obj:`str`

    """
    route = obj.API_NAME

    # if it's an ApiItem, all REST routes need the plural route, not the singular
    if isinstance(obj, api_models.ApiItem):
        route = obj.API_LIST_CLS.API_NAME

    if auto_target and target is None:
        if getattr(obj, "id", None) is not None:
            target = "{t}".format(t=obj.id)
        elif getattr(obj, "name", None) is not None:
            target = "by-name/{t}".format(t=obj.name)

    if needs_target and target is None:
        error = "A target is required for {o} and neither 'id' nor 'name' is set!"
        error = error.format(o=obj)
        raise exceptions.ModuleError(error)

    return build_endpoint(route, target)


def build_endpoint(route, target=None):
    """Build a REST endpoint string by joining route and target.

    Args:
        route (:obj:`str`):
            Route part of endpoint.
        target (:obj:`str`, optional):
            Target part of endpoint.

            Defaults to None.

    Returns:
        :obj:`str`

    """
    target = "" if target is None else "/{}".format(target)
    return "{}{}".format(route, target)


def check_adapter_types(adapter):
    """Check :meth:`Adapter.get_type` against api_client and objects type.

    Args:
        adapter (:obj:`Adapter`):
            Adapter to perform type checking on.

    Raises:
        :exc:`exceptions.TypeMismatchError`:
            If :meth:`Adapter.get_type` is not equal to
            :attr:`pytan3.api_objects.ApiObjects.module_type` or
            :meth:`pytan3.api_clients.ApiClient.get_type`.

    """
    if adapter.get_type() != adapter.api_objects.module_type:
        error = "{objects} does not match type of {adapter}"
        error = error.format(objects=adapter.api_objects, adapter=adapter)
        raise exceptions.TypeMismatchError(error)

    if adapter.get_type() != adapter.api_client.get_type():
        error = "{client} does not match type of {adapter}"
        error = error.format(client=adapter.api_client, adapter=adapter)
        raise exceptions.TypeMismatchError(error)


def check_adapter_version(adapter):
    """Check :meth:`Adapter.get_version_req` against api_client and objects version.

    Args:
        adapter (:obj:`Adapter`):
            Adapter to perform version checking on.

    Raises:
        :exc:`pytan3.utils.exceptions.VersionMismatchError`:
            If the version requirements from :meth:`Adapter.get_version_req` fail to
            match :attr:`pytan3.api_clients.ApiClient.version` or
            :attr:`pytan3.api_objects.ApiObjects.module_version`.

    """
    utils.versions.version_check_obj_req(
        version=adapter.api_client.version, src=adapter.api_client.url, obj=adapter
    )
    utils.versions.version_check_obj_req(
        version=adapter.api_objects.module_version, src=adapter.api_objects, obj=adapter
    )


def check_object_type(obj, types):
    """Check if an obj is an instance of types.

    Args:
        obj (:obj:`object`):
            Object to check against types.
        types (:obj:`tuple` of :obj:`type`):
            Types to check against obj.

    Raises:
        :exc:`exceptions.InvalidTypeError`:
            If type of obj is not on of types.

    """
    if not isinstance(obj, types):
        error = "Invalid object type {ot} - MUST be one of {at}"
        error = error.format(at=types, ot=type(obj))
        raise exceptions.InvalidTypeError(error)


def check_object_attrs(obj, attrs):
    """Check if any attributes of an obj are set.

    Args:
        obj (:obj:`pytan3.api_models.ApiModel`):
            API object to check.
        attrs (:obj:`list` of :obj:`str`):
            Attributes to check on obj.

    Raises:
        :exc:`exceptions.EmptyAttributeError`:
            If none of the attributes in attrs on obj are not set to None.

    """
    if isinstance(obj, api_models.ApiItem):
        if not any(getattr(obj, x, None) is not None for x in attrs):
            error = "No attributes in {a} defined on {o}"
            error = error.format(a=attrs, o=obj)
            raise exceptions.EmptyAttributeError(error)


def serialize_xml(obj, **kwargs):
    """Encode python object into an XML string.

    Args:
        obj (:obj:`object`):
            Python object to encode into a string.
        **kwargs:
            full_document (:obj:`bool`):
                Include xml stanza at top.

                Defaults to: True.
            pretty (:obj:`bool`):
                Indent the output doc.

                Defaults to: True.
            rest of kwargs:
                Passed to xmltodict.unparse.

    Returns:
        :obj:`str`

    """
    kwargs.setdefault("full_document", True)
    kwargs.setdefault("pretty", True)
    return xmltodict.unparse(obj, **kwargs)


def serialize_json(obj, **kwargs):
    """Encode python object into a JSON string.

    Args:
        obj (:obj:`object`):
            Python object to encode into a string.
        **kwargs:
            indent (:obj:`int`):
                Indent spacing for prettifying.

                Defaults to: 2.
            rest of kwargs:
                Passed to :func:`json.dumps`.

    Returns:
        :obj:`str`

    """
    kwargs.setdefault("indent", 2)
    return json.dumps(obj, **kwargs)


def load_type(obj=DEFAULT_TYPE):
    """Get a :class:`Adapter` by type from :meth:`Adapter.get_type`.

    Args:
        obj (:obj:`str`, optional):
            Type of Adapter.

            Defaults to: :data:`DEFAULT_TYPE`.

    Raises:
        :exc:`exceptions.ModuleError`:
            Unable to find a valid :class:`Adapter` with the supplied type.

    Returns:
        :class:`Adapter`

    """
    exp_cls = Adapter
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
    """Get a :class:`Adapter` by name from :meth:`Adapter.get_name`.

    Args:
        obj (:obj:`str` or :obj:`Adapter` or :class:`Adapter`, optional):
            Adapter object, class, or name Adapter.

            Defaults to: :data:`DEFAULT_NAME`.

    Raises:
        :exc:`exceptions.ModuleError`:
            Unable to find a valid :class:`Adapter` with the supplied name.

    Returns:
        :class:`Adapter`

    """
    exp_cls = Adapter
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

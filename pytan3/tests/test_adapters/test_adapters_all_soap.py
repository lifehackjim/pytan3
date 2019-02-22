# -*- coding: utf-8 -*-
"""Test suite for pytan3."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytan3
import pytest


class TestAdaptersAllSoap(object):
    """Test all Adapters of type: soap."""

    @pytest.fixture
    def adapter(self, adapter_soap, http_client, auth):
        """Get an adapter object of type: soap."""
        api_module = adapter_soap["api_module"]
        api_client_cls = adapter_soap["api_client"]
        adapter_cls = adapter_soap["adapter"]

        api_objects = pytan3.api_objects.ApiObjects(
            module_file=api_module["module_file"]
        )

        try:
            credentials_auth = pytan3.auth_methods.Credentials(
                http_client=http_client, **auth
            )
            api_client = api_client_cls(
                http_client=http_client, auth_method=credentials_auth
            )
            adapter = adapter_cls(api_client=api_client, api_objects=api_objects)
        except pytan3.api.exceptions.VersionMismatchError as exc:  # pragma: no cover
            m = "Skipping due to version requirement failure: {e}".format(e=exc)
            pytest.skip(m)
        return adapter

    # only SOAP has session returned
    def test_missing_session_warns(self, adapter, monkeypatch):
        """Test warn thrown when session element isn't found."""
        monkeypatch.setattr("pytan3.adapters.re_soap_tag", "x")
        user = adapter.api_objects.User(id=adapter.api_client.auth_method.uid)
        with pytest.warns(pytan3.adapters.exceptions.SessionNotFoundWarning):
            result = adapter.api_get(user)
        user = result()
        assert isinstance(result, pytan3.results.Soap)
        assert isinstance(user, adapter.api_objects.User)
        assert user.id == adapter.api_client.auth_method.uid
        assert user.name

    # only SOAP allows None for target
    def test_get_audit_logs_user_target_none(self, adapter):
        """Test type=user, target=None returns audit logs for all users."""
        result = adapter.api_get_audit_logs(type="user", target=None)
        logs = result()
        assert isinstance(result, pytan3.results.Soap)
        assert isinstance(logs, adapter.api_objects.AuditLog)
        assert isinstance(logs.entries, adapter.api_objects.AuditDataList)
        assert isinstance(logs.entries[0], adapter.api_objects.AuditData)
        assert len(logs.entries) > 1

    # SOAP and REST disagree on how audit logs should be returned. fun.
    def test_get_audit_logs_user_target(self, adapter):
        """Test type=user, target=auth_method.uid returns 1 audit log for 1 user."""
        target = adapter.api_client.auth_method.uid
        result = adapter.api_get_audit_logs(type="user", target=target)
        logs = result()
        assert isinstance(result, pytan3.results.Soap)
        assert isinstance(logs, adapter.api_objects.AuditLog)
        assert isinstance(logs.entries, adapter.api_objects.AuditDataList)
        assert isinstance(logs.entries[0], adapter.api_objects.AuditData)
        assert len(logs.entries) == 1

    def test_get_audit_logs_user_target_count2(self, adapter):
        """Test type=user, target=auth_method.uid, count=2 returns 2 audit log for 1 user."""
        target = adapter.api_client.auth_method.uid
        result = adapter.api_get_audit_logs(type="user", target=target, count=2)
        logs = result()
        assert isinstance(result, pytan3.results.Soap)
        assert isinstance(logs, adapter.api_objects.AuditLog)
        assert isinstance(logs.entries, adapter.api_objects.AuditDataList)
        assert isinstance(logs.entries[0], adapter.api_objects.AuditData)
        assert len(logs.entries) == 2

    def test_get_q_missing_attrs(self, adapter):
        """Test api_get w/ question with no attrs set works."""
        result = adapter.api_get(adapter.api_objects.Question())
        obj = result()
        assert isinstance(result, pytan3.results.Soap)
        assert isinstance(obj, adapter.api_objects.QuestionList)

    def test_bad_command(self, adapter):
        """Test exc thrown with cmd mismatch."""
        result = adapter.api_get(adapter.api_objects.User(id=adapter.auth_method.uid))

        obj = result.request_body_obj
        path = "soap:Envelope/soap:Body/t:tanium_soap_request"
        src = "SOAP API deserialized request body"

        request = result.get_dict_path(obj=obj, path=path, src=src)
        request["command"] = "badwolf"
        with pytest.raises(pytan3.results.exceptions.ResponseError):
            result()

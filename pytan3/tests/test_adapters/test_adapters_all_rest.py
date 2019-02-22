# -*- coding: utf-8 -*-
"""Test suite for pytan3."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytan3
import pytest


def test_magic_endpoint_item_empty(api_module_rest):
    """Test ApiItem no id or name set == plural endpoint and no target."""
    api_objects = pytan3.api_objects.ApiObjects(
        module_file=api_module_rest["module_file"]
    )
    obj = api_objects.User
    magic_endpoint = pytan3.adapters.magic_endpoint
    endpoint = magic_endpoint(obj=obj())
    assert endpoint == "users"


def test_magic_endpoint_item_id(api_module_rest):
    """Test ApiItem id no name set == plural endpoint and target of id."""
    api_objects = pytan3.api_objects.ApiObjects(
        module_file=api_module_rest["module_file"]
    )
    obj = api_objects.User
    magic_endpoint = pytan3.adapters.magic_endpoint
    endpoint = magic_endpoint(obj=obj(id=1))
    assert endpoint == "users/1"


def test_magic_endpoint_item_id_name(api_module_rest):
    """Test ApiItem id and name set == plural endpoint and target of id."""
    api_objects = pytan3.api_objects.ApiObjects(
        module_file=api_module_rest["module_file"]
    )
    obj = api_objects.User
    magic_endpoint = pytan3.adapters.magic_endpoint
    endpoint = magic_endpoint(obj=obj(id=1, name="x"))
    assert endpoint == "users/1"


def test_magic_endpoint_item_name(api_module_rest):
    """Test ApiItem name no id set == plural endpoint and target of name."""
    api_objects = pytan3.api_objects.ApiObjects(
        module_file=api_module_rest["module_file"]
    )
    obj = api_objects.User
    magic_endpoint = pytan3.adapters.magic_endpoint
    endpoint = magic_endpoint(obj=obj(name="x"))
    assert endpoint == "users/by-name/x"


def test_magic_endpoint_item_name_id_no_auto_target(api_module_rest):
    """Test ApiItem id and name set and auto_target=False == plural endpoint."""
    api_objects = pytan3.api_objects.ApiObjects(
        module_file=api_module_rest["module_file"]
    )
    obj = api_objects.User
    magic_endpoint = pytan3.adapters.magic_endpoint
    endpoint = magic_endpoint(obj=obj(id=1, name="x"), auto_target=False)
    assert endpoint == "users"


def test_magic_endpoint_item_empty_needs_target(api_module_rest):
    """Test exc thrown when ApiItem no id or name set and needs_target=True."""
    api_objects = pytan3.api_objects.ApiObjects(
        module_file=api_module_rest["module_file"]
    )
    obj = api_objects.User
    magic_endpoint = pytan3.adapters.magic_endpoint
    with pytest.raises(pytan3.adapters.exceptions.ModuleError):
        magic_endpoint(obj=obj(), needs_target=True)


def test_rest_url_path_missing_parts():
    """Test exc thrown when url is missing parts."""
    with pytest.raises(pytan3.results.exceptions.ModuleError):
        pytan3.results.RestUrlPath("https://badwolf")
    with pytest.raises(pytan3.results.exceptions.ModuleError):
        pytan3.results.RestUrlPath("https://badwolf/api")
    with pytest.raises(pytan3.results.exceptions.ModuleError):
        pytan3.results.RestUrlPath("https://badwolf/api/v2")


def test_rest_url_path_no_target():
    """Test url works with no target."""
    obj = pytan3.results.RestUrlPath("https://badwolf/api/v2/users")
    assert obj.route == "users"
    assert obj.target == ""
    assert obj.by_name is False


def test_rest_url_path_target():
    """Test url works with target."""
    obj = pytan3.results.RestUrlPath("https://badwolf/api/v2/users/1")
    assert obj.route == "users"
    assert obj.target == "1"
    assert obj.by_name is False


def test_rest_url_path_target_by_name():
    """Test url works with target."""
    obj = pytan3.results.RestUrlPath("https://badwolf/api/v2/users/by-name/bob")
    assert obj.route == "users"
    assert obj.target == "bob"
    assert obj.by_name is True
    assert "by-name=True" in format(obj)
    assert "by-name=True" in repr(obj)


@pytest.mark.needs_platform_version(min="7.3.314.3409")
class TestAdaptersAllRest(object):
    """Test all Adapters of type: rest."""

    @pytest.fixture
    def adapter(self, adapter_rest, http_client, auth):
        """Get an adapter object of type: rest."""
        api_module = adapter_rest["api_module"]
        api_client_cls = adapter_rest["api_client"]
        adapter_cls = adapter_rest["adapter"]

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

    def test_get_audit_logs_user_target(self, adapter):
        """Test type=user, target=auth_method.uid returns 1 audit log for 1 user."""
        target = adapter.api_client.auth_method.uid
        result = adapter.api_get_audit_logs(type="user", target=target)
        logs = result()
        assert isinstance(result, pytan3.results.Rest)
        assert isinstance(logs, adapter.api_objects.AuditLogList)
        assert isinstance(logs[0], adapter.api_objects.AuditLog)
        assert len(logs) == 1

    def test_get_audit_logs_user_target_count2(self, adapter):
        """Test type=user, target=auth_method.uid, count=2 returns 2 audit log for 1 user."""
        target = adapter.api_client.auth_method.uid
        result = adapter.api_get_audit_logs(type="user", target=target, count=2)
        logs = result()
        assert isinstance(result, pytan3.results.Rest)
        assert isinstance(logs, adapter.api_objects.AuditLogList)
        assert isinstance(logs[0], adapter.api_objects.AuditLog)
        assert len(logs) == 2

    def test_get_q_missing_attrs(self, adapter):
        """Test exc thrown in in api_get w/ question with no attrs set."""
        with pytest.raises(pytan3.adapters.exceptions.EmptyAttributeError):
            adapter.api_get(adapter.api_objects.Question())

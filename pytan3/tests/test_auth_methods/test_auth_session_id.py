# -*- coding: utf-8 -*-
"""Pass suite for pytan3.http_client.HttpClient."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytan3
import pytest


class TestAuthSessionId(object):
    """Test pytan3.auth_methods.SessionId."""

    def test_load_invalid(self):
        """Test exc thrown on load with invalid obj."""
        o = object()
        with pytest.raises(pytan3.auth_methods.exceptions.ModuleError):
            pytan3.auth_methods.load(o)

    def test_load_cls(self):
        """Test load works with SessionId class."""
        o = pytan3.auth_methods.SessionId
        cls = pytan3.auth_methods.load(o)
        assert issubclass(cls, pytan3.auth_methods.SessionId)

    def test_load_obj(self, http_client):
        """Test load works with SessionId obj."""
        auth = {"session": "1-1-1"}
        o = pytan3.auth_methods.SessionId(http_client=http_client, **auth)
        cls = pytan3.auth_methods.load(o)
        assert issubclass(cls, pytan3.auth_methods.SessionId)

    def test_load_store(self, http_client):
        """Test load works from AuthStore obj."""
        o = pytan3.auth_store.AuthStore(http_client=http_client, method="session_id")
        cls = pytan3.auth_methods.load(o)
        assert issubclass(cls, pytan3.auth_methods.SessionId)

    def test_load_str(self):
        """Test load works with "session_id"."""
        o = "session_id"
        cls = pytan3.auth_methods.load(o)
        assert issubclass(cls, pytan3.auth_methods.SessionId)

    def test_init(self, http_client, auth):
        """Test init, str, repr, get_name, get_type, get_args*."""
        creds = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        sauth = {"session": creds.token}
        method = pytan3.auth_methods.SessionId(http_client=http_client, **sauth)
        assert "logged_in=True" in format(method)
        assert "logged_in=True" in repr(method)
        assert method.get_name() == "session_id"
        assert method.get_args() == ["session"]
        assert method.get_args_required() == ["session"]
        assert method.get_args_secure() == []

    def test_to_store(self, http_client, auth):
        """Test create_store works."""
        creds = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        sauth = {"session": creds.token}
        method = pytan3.auth_methods.SessionId(http_client=http_client, **sauth)
        store = method.create_store()
        assert isinstance(store, pytan3.auth_store.AuthStore)
        assert store.get("session") == sauth["session"]

    def test_from_store(self, http_client, auth):
        """Test from_store works."""
        creds = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        store = pytan3.auth_store.AuthStore(
            http_client=http_client, method="session_id"
        )
        store.set("session", creds.token)
        method = pytan3.auth_methods.SessionId.from_store(store=store)
        assert isinstance(method, pytan3.auth_methods.SessionId)
        token = method.token
        assert pytan3.auth_methods.validate_token(token)
        assert "logged_in=True" in format(method)
        assert "logged_in=True" in repr(method)

    def test_login_notimpl(self, http_client, auth):
        """Test exc thrown on login."""
        creds = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        sauth = {"session": creds.token}
        method = pytan3.auth_methods.SessionId(http_client=http_client, **sauth)
        with pytest.raises(NotImplementedError):
            method.login()

    def test_expired_token_fails(self, http_client, auth):
        """Test exc thrown on expired token."""
        creds = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        sauth = {"session": creds.token}
        method = pytan3.auth_methods.SessionId(http_client=http_client, **sauth)
        method.token
        method.token = "1-1-badwolf"
        method._last_used = pytan3.utils.tools.secs_ago(method._expires_after + 5)
        with pytest.raises(pytan3.auth_methods.exceptions.InvalidToken):
            method.token
        with pytest.raises(pytan3.auth_methods.exceptions.InvalidToken):
            method.validate()

    def test_logout(self, http_client, auth):
        """Test logout works."""
        creds = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        sauth = {"session": creds.token}
        method = pytan3.auth_methods.SessionId(http_client=http_client, **sauth)
        method.token
        method.logout()

    def test_logout_invalid_token(self, http_client, auth):
        """Test exc thrown with logout and validate with invalid token."""
        sauth = {"session": "1-1-badwolf"}
        method = pytan3.auth_methods.SessionId(http_client=http_client, **sauth)
        with pytest.raises(pytan3.auth_methods.exceptions.InvalidToken):
            method.validate()
        with pytest.raises(pytan3.auth_methods.exceptions.LogoutError):
            method.logout()
        with pytest.raises(pytan3.auth_methods.exceptions.LogoutError):
            method.logout_all()

    def test_logout_error_after_logout(self, http_client, auth):
        """Test exc thrown with logout and validate after logged out."""
        creds = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        sauth = {"session": creds.token}
        method = pytan3.auth_methods.SessionId(http_client=http_client, **sauth)
        method.token
        method.logout()
        with pytest.raises(pytan3.auth_methods.exceptions.NotLoggedInError):
            method.logout()
        with pytest.raises(pytan3.auth_methods.exceptions.NotLoggedInError):
            method.validate()

    def test_validate_success(self, http_client, auth):
        """Test validate works."""
        creds = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        sauth = {"session": creds.token}
        method = pytan3.auth_methods.SessionId(http_client=http_client, **sauth)
        token1 = method.token
        token2 = method.validate()
        assert token1 == token2

    def test_version_check_fail(self, http_client, auth, monkeypatch):
        """Test exc thrown when vmin not met."""
        creds = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        sauth = {"session": creds.token}
        version_req = {"vmin": "7.3.314.3409", "vmax": "", "veq": ""}
        monkeypatch.setattr(
            pytan3.auth_methods.SessionId, "get_version_req", lambda x: version_req
        )
        monkeypatch.setattr("pytan3.api_clients.get_version", lambda x: "7.2.314.0000")
        with pytest.raises(pytan3.utils.exceptions.VersionMismatchError):
            pytan3.auth_methods.SessionId(http_client=http_client, **sauth)

    def test_version_check_false(self, http_client, auth, monkeypatch):
        """Test no exc thrown when vmin not met with ver_check=False."""
        creds = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        sauth = {"session": creds.token}
        version_req = {"vmin": "7.3.314.3409", "vmax": "", "veq": ""}
        monkeypatch.setattr(
            pytan3.auth_methods.SessionId, "get_version_req", lambda x: version_req
        )
        monkeypatch.setattr("pytan3.api_clients.get_version", lambda x: "7.2.314.0000")
        method = pytan3.auth_methods.SessionId(
            http_client=http_client, ver_check=False, **sauth
        )
        method.token

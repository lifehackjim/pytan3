# -*- coding: utf-8 -*-
"""Pass suite for pytan3.http_client.HttpClient."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytan3
import pytest


class TestAuthCredentials(object):
    """Test pytan3.auth_methods.Credentials."""

    def test_load_invalid(self):
        """Test exc thrown on load with invalid obj."""
        o = object()
        with pytest.raises(pytan3.auth_methods.exceptions.ModuleError):
            pytan3.auth_methods.load(o)

    def test_load_cls(self):
        """Test load works with Credentials class."""
        o = pytan3.auth_methods.Credentials
        cls = pytan3.auth_methods.load(o)
        assert issubclass(cls, pytan3.auth_methods.Credentials)

    def test_load_obj(self, http_client, auth):
        """Test load works with Credentials obj."""
        o = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        cls = pytan3.auth_methods.load(o)
        assert issubclass(cls, pytan3.auth_methods.Credentials)

    def test_load_store(self, http_client):
        """Test load works from AuthStore obj."""
        o = pytan3.auth_store.AuthStore(http_client=http_client, method="credentials")
        cls = pytan3.auth_methods.load(o)
        assert issubclass(cls, pytan3.auth_methods.Credentials)

    def test_load_str(self):
        """Test load works with "credentials"."""
        o = "credentials"
        cls = pytan3.auth_methods.load(o)
        assert issubclass(cls, pytan3.auth_methods.Credentials)

    def test_init(self, http_client, auth):
        """Test init, str, repr, get_name, get_type, get_args*."""
        method = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        assert "logged_in=False" in format(method)
        assert "logged_in=False" in repr(method)
        assert method.get_name() == "credentials"
        assert method.get_args() == ["username", "password", "secondary", "domain"]
        assert method.get_args_required() == ["username", "password"]
        assert method.get_args_secure() == ["password"]

    def test_to_store(self, http_client, auth):
        """Test create_store works."""
        method = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        store = method.create_store()
        assert isinstance(store, pytan3.auth_store.AuthStore)
        assert store.get("username") == auth["username"]
        assert store.get("password") == auth["password"]

    def test_from_store(self, http_client, auth):
        """Test from_store works."""
        method = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        store = pytan3.auth_store.AuthStore(
            http_client=http_client, method="credentials"
        )
        store.set("username", auth["username"])
        store.set("password", auth["password"])
        method = pytan3.auth_methods.Credentials.from_store(store=store)
        assert isinstance(method, pytan3.auth_methods.Credentials)
        token = method.token
        assert pytan3.auth_methods.validate_token(token)
        assert "logged_in=True" in format(method)
        assert "logged_in=True" in repr(method)

    def test_login_success(self, http_client, auth):
        """Test login works with valid creds."""
        method = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        token = method.token
        assert pytan3.auth_methods.validate_token(token)
        assert method.token_headers["session"] == token

    def test_login_failure(self, http_client):
        """Test login fails with invalid creds."""
        auth = {"username": "invalid", "password": "invalid"}
        method = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        with pytest.raises(pytan3.auth_methods.exceptions.LoginError):
            method.token

    def test_relogin_expired_token(self, http_client, auth):
        """Test expired token automatically gets new token."""
        method = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        token1 = method.token
        method._last_used = pytan3.utils.tools.secs_ago(method._expires_after + 5)
        token2 = method.token
        assert token1 != token2

    def test_relogin_invalid_token(self, http_client, auth):
        """Test invalid token automatically gets new token."""
        method = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        token1 = method.token
        method.token = "1-1-badwolf"
        method._last_used = pytan3.utils.tools.secs_ago(method.revalidate_after + 5)
        token2 = method.token
        assert token1 != token2

    def test_logout(self, http_client, auth):
        """Test logout works."""
        method = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        token1 = method.token
        method.logout()
        method.token = token1
        with pytest.raises(pytan3.auth_methods.exceptions.InvalidToken):
            method.validate()
        with pytest.raises(pytan3.auth_methods.exceptions.LogoutError):
            method.logout()

    def test_logout_invalid_token(self, http_client, auth):
        """Test exc thrown with logout and validate with invalid token."""
        method = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        method.token = "1-1-badwolf"
        with pytest.raises(pytan3.auth_methods.exceptions.InvalidToken):
            method.validate()
        with pytest.raises(pytan3.auth_methods.exceptions.LogoutError):
            method.logout()

    def test_logout_error_after_logout(self, http_client, auth):
        """Test exc thrown with logout and validate after logged out."""
        method = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        method.token
        method.logout()
        with pytest.raises(pytan3.auth_methods.exceptions.NotLoggedInError):
            method.logout()
        with pytest.raises(pytan3.auth_methods.exceptions.NotLoggedInError):
            method.validate()

    def test_logout_all(self, http_client, auth):
        """Test logout all works."""
        method1 = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        token1 = method1.token
        method2 = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        token2 = method2.token
        assert token1 != token2
        method1.logout_all()
        with pytest.raises(pytan3.auth_methods.exceptions.NotLoggedInError):
            method1.logout_all()
        with pytest.raises(pytan3.auth_methods.exceptions.NotLoggedInError):
            method1.logout()
        with pytest.raises(pytan3.auth_methods.exceptions.NotLoggedInError):
            method1.validate()
        with pytest.raises(pytan3.auth_methods.exceptions.InvalidToken):
            method2.validate()
        with pytest.raises(pytan3.auth_methods.exceptions.LogoutError):
            method2.logout()
        with pytest.raises(pytan3.auth_methods.exceptions.LogoutError):
            method2.logout_all()

    def test_validate_success(self, http_client, auth):
        """Test validate works."""
        method = pytan3.auth_methods.Credentials(http_client=http_client, **auth)
        token1 = method.token
        token2 = method.validate()
        assert token1 == token2

    def test_version_check_fail(self, http_client, auth, monkeypatch):
        """Test exc thrown when vmin not met."""
        version_req = {"vmin": "7.3.314.3409", "vmax": "", "veq": ""}
        monkeypatch.setattr(
            pytan3.auth_methods.Credentials, "get_version_req", lambda x: version_req
        )
        monkeypatch.setattr("pytan3.api_clients.get_version", lambda x: "7.2.314.0000")
        with pytest.raises(pytan3.utils.exceptions.VersionMismatchError):
            pytan3.auth_methods.Credentials(http_client=http_client, **auth)

    def test_version_check_false(self, http_client, auth, monkeypatch):
        """Test no exc thrown when vmin not met with ver_check=False."""
        version_req = {"vmin": "7.3.314.3409", "vmax": "", "veq": ""}
        monkeypatch.setattr(
            pytan3.auth_methods.Credentials, "get_version_req", lambda x: version_req
        )
        monkeypatch.setattr("pytan3.api_clients.get_version", lambda x: "7.2.314.0000")
        method = pytan3.auth_methods.Credentials(
            http_client=http_client, ver_check=False, **auth
        )
        method.token

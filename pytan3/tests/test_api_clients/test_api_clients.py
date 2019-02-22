# -*- coding: utf-8 -*-
"""Test suite for pytan3.api_clients."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import pytan3
import six


def test_load_invalid():
    """Test exc thrown on load with invalid obj."""
    o = object()
    with pytest.raises(pytan3.api_clients.exceptions.ModuleError):
        pytan3.api_clients.load(o)


def test_load_type_invalid():
    """Test exc thrown on load with invalid str."""
    o = "bad"
    with pytest.raises(pytan3.api_clients.exceptions.ModuleError):
        pytan3.api_clients.load_type(o)


def test_load_type_rest():
    """Test load works with "rest"."""
    o = "rest"
    cls = pytan3.api_clients.load_type(o)
    assert cls.get_type() == o
    assert issubclass(cls, pytan3.api_clients.ApiClient)


def test_load_type_soap():
    """Test load works with "soap"."""
    o = "soap"
    cls = pytan3.api_clients.load_type(o)
    assert cls.get_type() == o
    assert issubclass(cls, pytan3.api_clients.ApiClient)


def test_get_wsdl(http_client):
    """Test get_wsdl returns xml."""
    wsdl = pytan3.api_clients.get_wsdl(http_client)
    assert "xml" in wsdl


class TestApiClientSoap(object):
    """Test pytan3.api_clients.Soap."""

    def test_load_cls(self):
        """Test load works with Soap class."""
        o = pytan3.api_clients.Soap
        cls = pytan3.api_clients.load(o)
        assert issubclass(cls, pytan3.api_clients.Soap)

    def test_load_obj(self):
        """Test load works with Soap obj."""
        o = pytan3.api_clients.Soap(http_client=None, auth_method=None)
        cls = pytan3.api_clients.load(o)
        assert issubclass(cls, pytan3.api_clients.Soap)

    def test_load_str(self):
        """Test load works with "soap"."""
        o = "soap"
        cls = pytan3.api_clients.load(o)
        assert issubclass(cls, pytan3.api_clients.Soap)

    def test_construct(self, http_client, auth):
        """Test init, str, repr, get_name, get_type, auth, url."""
        credentials_auth = pytan3.auth_methods.Credentials(
            http_client=http_client, **auth
        )
        api_client = pytan3.api_clients.Soap(
            http_client=http_client, auth_method=credentials_auth
        )
        assert http_client.url in format(api_client)
        assert http_client.url in repr(api_client)
        assert api_client.get_name() == "soap"
        assert api_client.get_type() == "soap"
        assert api_client.auth_method == credentials_auth
        assert api_client.url == credentials_auth.http_client.url


class TestApiClientRest(object):
    """Test pytan3.api_clients.Rest."""

    def test_load_cls(self):
        """Test load works with Rest class."""
        o = pytan3.api_clients.Rest
        cls = pytan3.api_clients.load(o)
        assert issubclass(cls, pytan3.api_clients.Rest)

    def test_load_obj(self):
        """Test load works with Rest obj."""
        o = pytan3.api_clients.Rest(http_client=None, auth_method=None, ver_check=False)
        cls = pytan3.api_clients.load(o)
        assert issubclass(cls, pytan3.api_clients.Rest)

    def test_load_str(self):
        """Test load works with "rest"."""
        o = "rest"
        cls = pytan3.api_clients.load(o)
        assert issubclass(cls, pytan3.api_clients.Rest)

    def test_construct(self, http_client, auth):
        """Test init, str, repr, get_name, get_type, auth, url."""
        credentials_auth = pytan3.auth_methods.Credentials(
            http_client=http_client, **auth
        )
        api_client = pytan3.api_clients.Rest(
            http_client=http_client, auth_method=credentials_auth, ver_check=False
        )
        assert http_client.url in format(api_client)
        assert http_client.url in repr(api_client)
        assert api_client.get_name() == "rest"
        assert api_client.get_type() == "rest"
        assert api_client.auth_method == credentials_auth
        assert api_client.url == credentials_auth.http_client.url


class TestApiClientSoapTypes(object):
    """Test all ApiClient of type "soap"."""

    def test_api_manual_get_user(self, http_client, auth, api_client_soap):
        """Test get user with manual request and response parsing."""
        credentials_auth = pytan3.auth_methods.Credentials(
            http_client=http_client, **auth
        )
        api_client = api_client_soap(
            http_client=http_client, auth_method=credentials_auth
        )
        body_dict = pytan3.adapters.soap_envelope(
            cmd="GetObject", obj={"user": {"id": credentials_auth.uid}}
        )
        body = pytan3.adapters.serialize_xml(body_dict)
        r = api_client(data=body)
        r_dict = pytan3.adapters.xmltodict.parse(r.text)
        assert isinstance(r_dict, dict)
        path = "soap:Envelope/soap:Body/t:return/result_object/user"
        u_dict = pytan3.utils.tools.get_dict_path(obj=r_dict, path=path)
        assert int(u_dict["id"]) == int(credentials_auth.uid)
        assert u_dict["name"] == credentials_auth._headers["username"]


@pytest.mark.needs_platform_version(min="7.3.314.3409")
class TestApiClientRestTypes(object):
    """Test all ApiClient of type "rest"."""

    def test_api_manual_get_user(self, http_client, auth, api_client_rest):
        """Test get user with manual request and response parsing."""
        credentials_auth = pytan3.auth_methods.Credentials(
            http_client=http_client, **auth
        )
        api_client = api_client_rest(
            http_client=http_client, auth_method=credentials_auth
        )
        r = api_client(endpoint="/users/{}".format(credentials_auth.uid))
        r_dict = r.json()
        assert isinstance(r_dict, dict)
        u_dict = r_dict["data"]
        assert int(u_dict["id"]) == int(credentials_auth.uid)
        assert u_dict["name"] == credentials_auth._headers["username"]


class TestApiClientAllTypes(object):
    """Test all ApiClient of any type."""

    def test_version_check_fail(self, http_client, auth, monkeypatch, api_client_any):
        """Test exc thrown when vmin not met."""
        credentials_auth = pytan3.auth_methods.Credentials(
            http_client=http_client, **auth
        )
        version_req = {"vmin": "7.3.314.3409", "vmax": "", "veq": ""}
        monkeypatch.setattr(api_client_any, "get_version_req", lambda x: version_req)
        monkeypatch.setattr("pytan3.api_clients.get_version", lambda x: "7.2.314.0000")
        with pytest.raises(pytan3.utils.exceptions.VersionMismatchError):
            api_client_any(http_client=http_client, auth_method=credentials_auth)

    def test_version_check_false(self, http_client, auth, monkeypatch, api_client_any):
        """Test no exc thrown when vmin not met with ver_check=False."""
        version_req = {"vmin": "7.3.314.3409", "vmax": "", "veq": ""}
        monkeypatch.setattr(api_client_any, "get_version_req", lambda x: version_req)
        monkeypatch.setattr("pytan3.api_clients.get_version", lambda x: "7.2.314.0000")
        credentials_auth = pytan3.auth_methods.Credentials(
            http_client=http_client, **auth
        )
        api_client = api_client_any(
            http_client=http_client, auth_method=credentials_auth, ver_check=False
        )
        version = api_client.version
        assert len(version.split(".")) == 4

    def test_get_version_fail_warns(
        self, http_client, auth, monkeypatch, api_client_any
    ):
        """Test warning on failure to get "serverVersion" from config attr."""
        credentials_auth = pytan3.auth_methods.Credentials(
            http_client=http_client, **auth
        )
        monkeypatch.setattr("pytan3.api_clients.get_config", lambda x: {})
        api_client = api_client_any(
            http_client=http_client, auth_method=credentials_auth, ver_check=False
        )
        with pytest.warns(pytan3.api_clients.exceptions.GetPlatformVersionWarning):
            version = api_client.version
            assert not version

    def test_get_version(self, http_client, auth, api_client_any):
        """Test "serverVersion" from config attr works."""
        credentials_auth = pytan3.auth_methods.Credentials(
            http_client=http_client, **auth
        )
        api_client = api_client_any(
            http_client=http_client, auth_method=credentials_auth, ver_check=False
        )
        version = api_client.version
        assert isinstance(version, six.string_types)
        assert "." in version

    def test_get_config(self, http_client, auth, api_client_any):
        """Test get_config from config attr."""
        credentials_auth = pytan3.auth_methods.Credentials(
            http_client=http_client, **auth
        )
        api_client = api_client_any(
            http_client=http_client, auth_method=credentials_auth, ver_check=False
        )
        config = api_client.config
        assert isinstance(config, dict)

    def test_get_info(self, http_client, auth, api_client_any):
        """Test get_info from info attr."""
        credentials_auth = pytan3.auth_methods.Credentials(
            http_client=http_client, **auth
        )
        api_client = api_client_any(
            http_client=http_client, auth_method=credentials_auth, ver_check=False
        )
        info = api_client.info
        assert isinstance(info, dict)

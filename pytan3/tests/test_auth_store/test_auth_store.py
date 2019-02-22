# -*- coding: utf-8 -*-
"""Test suite for pytan3.auth_store."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytan3
import pytest

# import input_mocker
# import getpass
# import six


class TestAuthStore(object):
    """Test pytan3.auth_store.AuthStore."""

    def test_construct(self, http_client):
        """Test construct."""
        store = pytan3.auth_store.AuthStore(http_client=http_client)
        assert "from={!r}".format("init") in format(store)
        assert "from={!r}".format("init") in repr(store)

    def test_get_req_key_missing(self, http_client):
        """Test exc thrown on get of missing required key."""
        store = pytan3.auth_store.AuthStore(http_client=http_client)
        with pytest.raises(pytan3.auth_store.exceptions.ModuleError):
            store.get("missing_key")

    def test_get_opt_key_missing(self, http_client):
        """Test no exc thrown on get of missing non-required key."""
        store = pytan3.auth_store.AuthStore(http_client=http_client)
        v = store.get("missing_key", False)
        assert v == ""

    def test_get_key(self, http_client):
        """Test no exc thrown on get of existing key."""
        store = pytan3.auth_store.AuthStore(http_client=http_client)
        store.set("another_key", "blah")
        v = store.get("another_key")
        assert v == "blah"

    def test_auth_store_secret(self, http_client):
        """Test secret combines cert and key sep by "__"."""
        s = "badwolf123"
        store = pytan3.auth_store.AuthStore(http_client=http_client, secret=s)
        v = store.secret
        assert "__" in v
        assert v.endswith(s)
        assert v.startswith(http_client.certify.store.pem)

    def test_auth_store_secret_b64(self, http_client):
        """Test b64 encoded secret prefixed "B####" works."""
        s = "badwolf123"
        sb64 = "B####" + pytan3.utils.tools.b64_encode(s)
        store = pytan3.auth_store.AuthStore(http_client=http_client, secret=sb64)
        v = store.secret
        assert "__" in v
        assert v.endswith(s)
        assert v.startswith(http_client.certify.store.pem)

    def test_create_method_auto(self, http_client, auth):
        """Test create_method from store works with default method."""
        store = pytan3.auth_store.AuthStore(http_client=http_client)
        store.set("username", auth["username"])
        store.set("password", auth["password"])
        method = store.create_method()
        assert isinstance(method, pytan3.auth_methods.Credentials)
        assert method._headers["username"] == auth["username"]
        assert method._headers["password"] == auth["password"]

    def test_create_method_manual(self, http_client, auth):
        """Test create_method from store works with supplied method."""
        store = pytan3.auth_store.AuthStore(
            http_client=http_client, method="session_id"
        )
        s = "1-111-1"
        store.set("session", s)
        method = store.create_method()
        assert isinstance(method, pytan3.auth_methods.SessionId)
        assert method._headers["session"] == s

    def test_tofrom_stream(self, http_client, auth):
        """Test to/from stream works."""
        store = pytan3.auth_store.AuthStore(http_client=http_client)
        store.set("username", auth["username"])
        store.set("password", auth["password"])
        stream = store.to_stream()
        v = stream.getvalue()
        assert "::CSC::" in v
        back = pytan3.auth_store.AuthStore.from_stream(http_client, stream)
        assert back.get("username") == store.get("username")
        assert back.get("password") == store.get("password")
        assert back.method == store.method

    def test_tofrom_string(self, http_client, auth):
        """Test to/from string works."""
        store = pytan3.auth_store.AuthStore(http_client=http_client)
        store.set("username", auth["username"])
        store.set("password", auth["password"])
        v = store.to_string()
        assert "::CSC::" in v
        back = pytan3.auth_store.AuthStore.from_string(
            http_client=http_client, string=v
        )
        assert back.get("username") == store.get("username")
        assert back.get("password") == store.get("password")
        assert back.method == store.method

    def test_tofrom_path(self, http_client, tmp_path, auth):
        """Test to/from path works."""
        store = pytan3.auth_store.AuthStore(http_client=http_client)
        store.set("username", auth["username"])
        store.set("password", auth["password"])
        path = store.to_path(path=tmp_path)
        assert path.is_file()
        back = pytan3.auth_store.AuthStore.from_path(
            http_client=http_client, path=tmp_path
        )
        assert back.get("username") == store.get("username")
        assert back.get("password") == store.get("password")
        assert back.method == store.method

    def test_to_path_exists_over_false(self, http_client, tmp_path, auth):
        """Test exc thrown when to_path store exists and overwrite is default."""
        store = pytan3.auth_store.AuthStore(http_client=http_client)
        store.set("username", auth["username"])
        store.set("password", auth["password"])
        store.to_path(path=tmp_path)
        with pytest.raises(pytan3.auth_store.exceptions.ModuleError):
            store.to_path(path=tmp_path)

    def test_to_path_exists_over_true(self, http_client, tmp_path, auth):
        """Test warn when to_path store exists and overwrite is True."""
        store = pytan3.auth_store.AuthStore(http_client=http_client)
        store.set("username", auth["username"])
        store.set("password", auth["password"])
        store.to_path(path=tmp_path)
        with pytest.warns(pytan3.auth_store.exceptions.ModuleWarning):
            store.to_path(path=tmp_path, overwrite=True)

    def test_to_path_exists_over_none(self, http_client, tmp_path, auth):
        """Test warn when to_path store exists and overwrite is None."""
        store = pytan3.auth_store.AuthStore(http_client=http_client)
        store.set("username", auth["username"])
        store.set("password", auth["password"])
        path1 = store.to_path(path=tmp_path)
        store.set("password", "moo")
        with pytest.warns(pytan3.auth_store.exceptions.ModuleWarning):
            path2 = store.to_path(path=tmp_path, overwrite=None)
        contents1 = path1.read_text()
        contents2 = path2.read_text()
        assert contents1 == contents2

    def test_from_badpath(self, http_client, tmp_path):
        """Test exc thrown when from_path cant find store."""
        with pytest.raises(pytan3.auth_store.exceptions.ModuleError):
            pytan3.auth_store.AuthStore.from_path(http_client, path=tmp_path)


# TODO(!) figure out once prompting land entered again
#     def test_from_prompts(self, http_client, monkeypatch):
#         """Pass."""
#         monkeypatch.setattr(getpass, "getpass", six.moves.input)
#         monkeypatch.setattr("pytan3.utils.prompts.promptness._ignore_notty", True)
#         inputs = [
#             "credentials",
#             "y",
#             "customsecret",
#             "validuser",
#             "validpass",
#             "validsec",
#             "validdom",
#         ]
#         with input_mocker.InputMocker(inputs=inputs):
#             store = pytan3.auth_store.AuthStore.from_prompts(http_client)
#         assert isinstance(store, pytan3.auth_store.AuthStore)
#         assert store.get("username") == "validuser"
#         assert store.get("password") == "validpass"
#         assert store.get("secondary") == "validsec"
#         assert store.get("domain") == "validdom"
#         assert store.method == pytan3.auth_methods.Credentials
#         assert "customsecret" in store.secret.splitlines()[-1]
#         assert "BEGIN CERTIFICATE" in store.secret.splitlines()[0]

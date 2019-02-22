# -*- coding: utf-8 -*-
"""Test suite for pytan3.http_client.HttpClient."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import httpretty
import input_mocker
import json
import logging
import os
import pytan3
import pytest
import requests
import shutil


class TestHttpClient(object):
    """Test pytan3.http_client.HttpClient."""

    def test_custom_cert(self, caplog, httpsbin_cert, log_check):
        """Test specify a custom path and path file to cert works."""
        caplog.set_level(logging.DEBUG)
        server, example_cert = httpsbin_cert
        url = server()
        path = format(example_cert.parent.parent)
        path_file = format(example_cert.name)
        http_client = pytan3.http_client.HttpClient(url=url, lvl="debug")
        http_client.certify(path=path, path_file=path_file, lvl="debug")

        r = http_client()
        assert http_client.certify.store.subject == {"common_name": "example.com"}
        assert http_client.url in format(http_client)
        assert http_client.url in repr(http_client)
        assert path_file in format(http_client.certify)
        assert path_file in repr(http_client.certify)
        assert isinstance(r, requests.Response)
        entries = [
            "Default certificate for .*? is not valid, will find/get one",
            "Certificate at .*? is valid for URL",
        ]
        log_check(caplog, entries)

    def test_hostname_cert(self, caplog, tmp_path, httpsbin_cert, log_check):
        """Test supplying no path_file finds hostname based cert in path."""
        caplog.set_level(logging.DEBUG)
        server, example_cert = httpsbin_cert
        url = server()
        url_parsed = requests.compat.urlparse(url)
        path = tmp_path
        certs_path = path / "certs"
        certs_path.mkdir(parents=True, exist_ok=True)
        host_cert_file = "{}.pem".format(url_parsed.hostname)
        host_cert_path = certs_path / host_cert_file
        shutil.copy(format(example_cert), format(host_cert_path))

        http_client = pytan3.http_client.HttpClient(url=url, lvl="debug")
        http_client.certify(path=path, lvl="debug")
        http_client()
        assert http_client.certify.store.subject == {"common_name": "example.com"}
        entries = [
            "Default certificate for .*? is not valid, will find/get one",
            "Certificate at .*? is valid for URL",
        ]
        log_check(caplog, entries)

    def test_already_valid_cert(self, caplog, httpsbin_cert, log_check):
        """Test OS env based cert file works with out specifying path/path_file."""
        caplog.set_level(logging.DEBUG)
        server, example_cert = httpsbin_cert
        url = server()
        os.environ["REQUESTS_CA_BUNDLE"] = format(example_cert)

        http_client = pytan3.http_client.HttpClient(url=url, lvl="debug")
        http_client.certify(lvl="debug")
        http_client()
        del (os.environ["REQUESTS_CA_BUNDLE"])
        assert http_client.certify.store.subject == {"common_name": "example.com"}
        entries = ["Default certificate for .*? is valid, not setting custom cert."]
        log_check(caplog, entries)

    def test_missing_cert_user_yes(
        self, caplog, capsys, tmp_path, httpsbin_cert, log_check, monkeypatch
    ):
        """Test use saying yes to is cert valid works."""
        caplog.set_level(logging.DEBUG)
        server, example_cert = httpsbin_cert
        url = server()
        monkeypatch.setattr("pytan3.http_client.SHOW_CERT", "yes")
        monkeypatch.setattr("pytan3.http_client.SHOW_CHAIN", "yes")
        monkeypatch.setattr("pytan3.http_client.CERT_VALID", "yes")
        with pytest.warns(pytan3.http_client.exceptions.CertificateNotFoundWarning):
            with capsys.disabled():
                inputs = ["y", "y", "y"]
                with input_mocker.InputMocker(inputs=inputs):
                    http_client = pytan3.http_client.HttpClient(url=url, lvl="debug")
                    http_client.certify(path=tmp_path, lvl="debug")
        assert http_client.certify.store.subject == {"common_name": "example.com"}
        entries = ["Wrote certificate for"]
        log_check(caplog, entries)

    def test_missing_cert_osenv_yes(
        self, caplog, capsys, tmp_path, httpsbin_cert, log_check
    ):
        """Test setting PYTAN_CERT_VALID env var makes valid prompt default=yes."""
        caplog.set_level(logging.DEBUG)
        server, example_cert = httpsbin_cert
        url = server()
        os.environ["PYTAN_CERT_VALID"] = "y"
        with pytest.warns(pytan3.http_client.exceptions.CertificateNotFoundWarning):
            with capsys.disabled():
                inputs = ["", "", ""]
                with input_mocker.InputMocker(inputs=inputs):
                    http_client = pytan3.http_client.HttpClient(url=url, lvl="debug")
                    http_client.certify(path=tmp_path, lvl="debug")
        del (os.environ["PYTAN_CERT_VALID"])
        assert http_client.certify.store.subject == {"common_name": "example.com"}
        entries = ["Wrote certificate for"]
        log_check(caplog, entries)

    def test_missing_cert_verify_hook_false(
        self, caplog, tmp_path, httpsbin_cert, log_check
    ):
        """Test verify_hook=False does not do validity prompting."""
        caplog.set_level(logging.DEBUG)
        server, example_cert = httpsbin_cert
        url = server()
        with pytest.warns(pytan3.http_client.exceptions.CertificateNotFoundWarning):
            http_client = pytan3.http_client.HttpClient(url=url, lvl="debug")
            http_client.certify(path=tmp_path, verify_hook=False, lvl="debug")
        assert http_client.certify.store.subject == {"common_name": "example.com"}
        entries = ["Wrote certificate for"]
        log_check(caplog, entries)

    def test_missing_cert_user_no(self, tmp_path, httpsbin_cert):
        """Test exc thrown when user says no to validity prompt."""
        server, example_cert = httpsbin_cert
        url = server()
        with pytest.warns(pytan3.http_client.exceptions.CertificateNotFoundWarning):
            with pytest.raises(pytan3.http_client.exceptions.CertificateInvalidError):
                inputs = ["n", "n", "n"]
                with input_mocker.InputMocker(inputs=inputs):
                    http_client = pytan3.http_client.HttpClient(url=url, lvl="debug")
                    http_client.certify(path=tmp_path, lvl="debug")

    def test_invalid_cert(self, httpsbin_cert, other_cert):
        """Test exc thrown if wrong cert provided."""
        server, example_cert = httpsbin_cert
        url = server()
        path_file = format(other_cert.name)
        path = format(other_cert.parent.parent)
        with pytest.raises(pytan3.http_client.exceptions.CertificateInvalidError):
            http_client = pytan3.http_client.HttpClient(url=url, lvl="debug")
            http_client.certify(path=path, path_file=path_file, lvl="debug")

    def test_record_history(self, httpsbin_cert):
        """Test record_history adds responses to history attr."""
        server, example_cert = httpsbin_cert
        url = server()
        path = format(example_cert.parent.parent)
        path_file = format(example_cert.name)
        http_client = pytan3.http_client.HttpClient(url=url, lvl="debug")
        http_client.certify(path=path, path_file=path_file, lvl="debug")

        http_client.control_hook_record_history(enable=True)
        r = http_client()
        assert r in http_client.history
        http_client.control_hook_record_history(enable=False)
        r = http_client()
        assert r not in http_client.history

    def test_record_disk(self, httpsbin_cert, tmp_path):
        """Test record_disk writes responses to disk as json."""
        server, example_cert = httpsbin_cert
        url = server()
        path = format(example_cert.parent.parent)
        path_file = format(example_cert.name)
        http_client = pytan3.http_client.HttpClient(url=url, lvl="debug")
        http_client.certify(path=path, path_file=path_file, lvl="debug")

        http_client.control_hook_record_disk(enable=True, path=tmp_path)
        r = http_client()
        assert hasattr(r, "record_path")
        assert r.record_path.is_file()
        assert json.loads(r.record_path.read_text())
        http_client.control_hook_record_disk(enable=False)
        r = http_client()
        assert not hasattr(r, "record_path")

    def test_clean_auth(self):
        """Test headers get cleaned in request to auth api."""
        httpretty.enable()
        httpretty.register_uri(
            method=httpretty.POST,
            uri="http://pytantest:443/auth",
            body="session",
            status=200,
        )

        http_client = pytan3.http_client.HttpClient(url="http://pytantest:443")
        headers = {"username": "dunder"}
        r = http_client(method="post", path="auth", headers=headers)
        assert r.request.clean_headers["username"] == "###HIDDEN###"
        httpretty.disable()
        httpretty.reset()

    def test_clean_auth_rest(self):
        """Test headers get cleaned in request to rest session api."""
        httpretty.enable()
        response_body = json.dumps({"text": {"session": "moo"}})
        httpretty.register_uri(
            method=httpretty.POST,
            uri="http://pytantest:443/api/v2/session/login",
            body=response_body,
            status=200,
        )

        http_client = pytan3.http_client.HttpClient(url="http://pytantest:443")
        # bytes so no pyopenssl warning on py2  # TODO(!) in client??
        body = json.dumps({"username": "dunder"})
        r = http_client(method="post", path="/api/v2/session/login", data=body)
        clean_body = json.loads(r.request.clean_body)
        assert clean_body["username"] == "###HIDDEN###"
        httpretty.disable()
        httpretty.reset()

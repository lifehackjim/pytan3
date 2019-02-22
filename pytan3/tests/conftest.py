# -*- coding: utf-8 -*-
"""Conf for py.test."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import pytest
import pytan3
import pytest_httpbin.certs
import pytest_httpbin.serve
from requests.compat import urljoin
import re
from pytest_lazyfixture import lazy_fixture

try:
    import pathlib
except ImportError:  # pragma: no cover
    import pathlib2 as pathlib

THIS_DIR = pathlib.Path(__file__).absolute().parent

PYTAN_URL = os.environ.get("PYTAN_URL", None) or None
PYTAN_USERNAME = os.environ.get("PYTAN_USERNAME", None) or None
PYTAN_PASSWORD = os.environ.get("PYTAN_PASSWORD", None) or None

API_MODULES_SOAP = pytan3.api_objects.get_versions("soap")
API_MODULES_REST = pytan3.api_objects.get_versions("rest")
API_MODULES_ALL = API_MODULES_SOAP + API_MODULES_REST

API_CLIENTS_ALL = pytan3.api_clients.ApiClient.__subclasses__()
API_CLIENTS_REST = [x for x in API_CLIENTS_ALL if x.get_type() == "rest"]
API_CLIENTS_SOAP = [x for x in API_CLIENTS_ALL if x.get_type() == "soap"]

ADAPTERS_ALL = pytan3.adapters.Adapter.__subclasses__()
ADAPTERS_REST = [x for x in ADAPTERS_ALL if x.get_type() == "rest"]
ADAPTERS_SOAP = [x for x in ADAPTERS_ALL if x.get_type() == "soap"]
promptness = pytan3.utils.prompts.promptness


def pytest_addoption(parser):
    """Pass."""
    parser.addoption(
        "--url",
        action="store",
        default=PYTAN_URL,
        required=False,
        help="url of tanium server",
    )
    parser.addoption(
        "--username",
        action="store",
        default=PYTAN_USERNAME,
        required=False,
        help="url of tanium server",
    )
    parser.addoption(
        "--password",
        action="store",
        default=PYTAN_PASSWORD,
        required=False,
        help="url of tanium server",
    )


@pytest.fixture(scope="session")
def http_client(request):
    """Pass."""
    url = request.config.getoption("--url")
    url = url or promptness.ask_str(
        text="Provide Tanium URL", default=None, env_var="PYTAN_URL"
    )
    client = pytan3.http_client.HttpClient(url=url)
    client.certify()
    return client


@pytest.fixture(scope="session")
def auth(request):
    """Pass."""
    username = request.config.getoption("--username")
    username = username or promptness.ask_str(
        text="Provide Tanium Administrator Username",
        default="Administrator",
        env_var="PYTAN_USERNAME",
    )
    password = request.config.getoption("--password")
    password = password or promptness.ask_str(
        text="Provide Tanium Administrator Password",
        secure=True,
        env_var="PYTAN_PASSWORD",
    )
    auth = {"username": username, "password": password}
    return auth


@pytest.fixture(scope="session")
def platform_version(http_client):
    """Pass."""
    return pytan3.api_clients.get_version(http_client)


@pytest.fixture(autouse=True)
def check_needs_platform_version(request, platform_version):
    """Pass."""
    needs_ver = request.node.get_closest_marker("needs_platform_version")
    if needs_ver:
        vmin = needs_ver.kwargs.get("min")
        vmax = needs_ver.kwargs.get("max")
        veq = needs_ver.kwargs.get("eq")
        fails_vmin = vmin and not pytan3.utils.versions.version_min(
            v1=platform_version, v2=vmin
        )
        fails_vmax = vmax and not pytan3.utils.versions.version_max(
            v1=platform_version, v2=vmax
        )
        fails_veq = veq and not pytan3.utils.versions.version_eq(
            v1=platform_version, v2=veq
        )
        if fails_vmin:  # pragma: no cover
            m = "skipped due to platform v{v1} less than v{v2}"
            m = m.format(v1=platform_version, v2=vmin)
            pytest.skip(m)
        if fails_vmax:  # pragma: no cover
            m = "skipped due to platform v{v1} greater than v{v2}"
            m = m.format(v1=platform_version, v2=vmax)
            pytest.skip(m)
        if fails_veq:  # pragma: no cover
            m = "skipped due to platform v{v1} not equals v{v2}"
            m = m.format(v1=platform_version, v2=veq)
            pytest.skip(m)


def prepare_url(value):
    """Pass."""
    httpbin_url = value.url.rstrip("/") + "/"

    def inner(*suffix):
        return urljoin(httpbin_url, "/".join(suffix))

    return inner


@pytest.fixture
def httpsbin_cert(monkeypatch, example_cert, httpbin_secure):
    """Pass."""
    monkeypatch.setattr(pytest_httpbin.serve, "CERT_DIR", format(example_cert.parent))
    return (prepare_url(httpbin_secure), example_cert)


@pytest.fixture
def cert_dir():
    """Pass."""
    return THIS_DIR / "certs"


def check_cert_path(path):
    """Pass."""
    build_path = path.parent / "build_certs.py"
    if not path.is_file():
        error = "Cert {path!r} does not exist, run {build_path!r}"
        error = error.format(path=format(path), build_path=format(build_path))
        raise Exception(error)


@pytest.fixture
def example_cert(cert_dir):
    """Pass."""
    path = cert_dir / "cert.pem"
    check_cert_path(path)
    return path


@pytest.fixture
def other_cert(cert_dir):
    """Pass."""
    path = cert_dir / "othercert.pem"
    check_cert_path(path)
    return path


@pytest.fixture
def log_check():
    """Pass."""
    # moo
    def _log_check(caplog, entries):
        """Pass."""
        msgs = [rec.message for rec in caplog.records]
        for entry in entries:
            if not any(re.search(entry, m) for m in msgs):  # pragma: no cover
                error = "Did not find entry in log: {!r}\nAll entries:\n{}"
                error = error.format(entry, "\n".join(msgs))
                raise Exception(error)

    return _log_check


@pytest.fixture(params=API_MODULES_SOAP)
def api_module_soap(request):
    """Pass."""
    return request.param


@pytest.fixture(params=API_MODULES_REST)
def api_module_rest(request):
    """Pass."""
    return request.param


@pytest.fixture(params=API_MODULES_ALL)
def api_module_any(request):
    """Pass."""
    return request.param


@pytest.fixture(params=API_CLIENTS_REST)
def api_client_rest(request):
    """Pass."""
    return request.param


@pytest.fixture(params=API_CLIENTS_SOAP)
def api_client_soap(request):
    """Pass."""
    return request.param


@pytest.fixture(params=API_CLIENTS_ALL)
def api_client_any(request):
    """Pass."""
    return request.param


@pytest.fixture(params=ADAPTERS_REST)
def adapter_rest(request, api_module_rest, api_client_rest):
    """Pass."""
    return {
        "adapter": request.param,
        "api_module": api_module_rest,
        "api_client": api_client_rest,
    }


@pytest.fixture(params=ADAPTERS_SOAP)
def adapter_soap(request, api_module_soap, api_client_soap):
    """Pass."""
    return {
        "adapter": request.param,
        "api_module": api_module_soap,
        "api_client": api_client_soap,
    }


@pytest.fixture(params=[lazy_fixture("adapter_rest"), lazy_fixture("adapter_soap")])
def adapter_any(request):
    """Pass."""
    return request.param

# -*- coding: utf-8 -*-
"""Test suite for pytan3."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytan3

# import pytest


class TestAdapterSoap(object):
    """Test pytan3.adapters.Soap."""

    def test_load_str(self):
        """Test load with "soap" str returns this class."""
        o = "soap"
        cls = pytan3.adapters.load(o)
        assert issubclass(cls, pytan3.adapters.Soap)

    def test_init(self, api_module_soap, http_client, auth):
        """Test init, str, repr, and properties."""
        api_objects = pytan3.api_objects.ApiObjects(
            module_file=api_module_soap["module_file"]
        )
        credentials_auth = pytan3.auth_methods.Credentials(
            http_client=http_client, **auth
        )
        api_client = pytan3.api_clients.Soap(
            http_client=http_client, auth_method=credentials_auth
        )
        adapter = pytan3.adapters.Soap(api_client=api_client, api_objects=api_objects)
        assert adapter.api_client == api_client
        assert adapter.http_client == http_client
        assert adapter.api_objects == api_objects
        assert adapter.auth_method == credentials_auth
        assert adapter.get_name() == "soap"
        assert adapter.get_type() == "soap"
        assert adapter.result_cls == pytan3.results.Soap
        assert format(http_client) in format(adapter)
        assert format(http_client) in repr(adapter)
        cls = pytan3.adapters.load(adapter)
        assert issubclass(cls, pytan3.adapters.Soap)

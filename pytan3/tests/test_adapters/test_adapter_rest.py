# -*- coding: utf-8 -*-
"""Test suite for pytan3."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytan3
import pytest


@pytest.mark.needs_platform_version(min="7.3.314.3409")
class TestAdapterRest(object):
    """Test pytan3.adapters.Rest."""

    def test_load_str(self):
        """Test load with "rest" str returns this class."""
        o = "rest"
        cls = pytan3.adapters.load(o)
        assert issubclass(cls, pytan3.adapters.Rest)

    def test_init(self, api_module_rest, http_client, auth):
        """Test init, str, repr, and properties."""
        credentials_auth = pytan3.auth_methods.Credentials(
            http_client=http_client, **auth
        )
        api_objects = pytan3.api_objects.ApiObjects(
            module_file=api_module_rest["module_file"]
        )
        api_client = pytan3.api_clients.Rest(
            http_client=http_client, auth_method=credentials_auth
        )
        adapter = pytan3.adapters.Rest(api_client=api_client, api_objects=api_objects)
        assert adapter.get_name() == "rest"
        assert adapter.get_type() == "rest"
        assert adapter.api_client == api_client
        assert adapter.http_client == http_client
        assert adapter.api_objects == api_objects
        assert adapter.auth_method == credentials_auth
        assert adapter.result_cls == pytan3.results.Rest
        assert format(http_client) in format(adapter)
        assert format(http_client) in repr(adapter)
        cls = pytan3.adapters.load(adapter)
        assert issubclass(cls, pytan3.adapters.Rest)

# -*- coding: utf-8 -*-
"""Test suite for pytan3."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import pytan3
import pytest

# import six


def test_bad_type():
    """Test exc thrown on load with bad api type."""
    with pytest.raises(pytan3.api_objects.exceptions.ModuleError):
        pytan3.api_objects.load(api_type="moo")


def test_auto_load():
    """Test load works with defaults."""
    obj = pytan3.api_objects.load()
    assert isinstance(obj, pytan3.api_objects.ApiObjects)


def test_get_versions_empty():
    """Test exc thrown with no versions found for api type."""
    with pytest.raises(pytan3.api_objects.exceptions.NoVersionFoundError):
        pytan3.api_objects.get_versions(api_type="notknot")


def test_find_version_no_match():
    """Test exc thrown when no matching versions found."""
    with pytest.raises(pytan3.api_objects.exceptions.NoVersionFoundError):
        pytan3.api_objects.find_version(veq="9.9.9.9")


class TestApiObjects(object):
    """Pass."""

    @pytest.fixture
    def api_objects(self, api_module_any):
        """Fixture to get pytan3.api_objects.ApiObjects obj."""
        return pytan3.api_objects.ApiObjects(module_file=api_module_any["module_file"])

    def test_properties(self, api_objects, api_module_any):
        """Test properties of ApiObjects instances."""
        assert api_objects.module_type in format(api_objects)
        assert api_objects.module_type in repr(api_objects)
        assert issubclass(api_objects.ApiModel, pytan3.api_models.ApiModel)
        assert issubclass(api_objects.ApiItem, pytan3.api_models.ApiItem)
        assert issubclass(api_objects.ApiList, pytan3.api_models.ApiList)
        assert api_objects.module_dt == api_objects.module.API_DT
        assert api_objects.module_type == api_objects.module.TYPE
        assert api_objects.module_type == api_module_any["api_type"]
        assert api_objects.module_version == api_module_any["ver_str"]
        assert api_objects.module_version_dict["string"] == api_module_any["ver_str"]
        assert isinstance(api_objects.cls_item, list)
        assert isinstance(api_objects.cls_list, list)
        assert isinstance(api_objects.cls_all, list)
        assert isinstance(api_objects.cls_name_map_item, dict)
        assert isinstance(api_objects.cls_name_map_list, dict)
        assert isinstance(api_objects.cls_name_map_all, dict)

    def test_dupe_name_map(self, api_objects, api_module_any, monkeypatch):
        """Test exc thrown on duplicate API names of ApiObjects."""
        monkeypatch.setattr(api_objects.Group, "API_NAME", "user")
        monkeypatch.setattr(api_objects.GroupList, "API_NAME", "users")
        with pytest.raises(pytan3.api_objects.exceptions.ModuleError):
            api_objects.cls_name_map_item
        with pytest.raises(pytan3.api_objects.exceptions.ModuleError):
            api_objects.cls_name_map_list
        with pytest.raises(pytan3.api_objects.exceptions.ModuleError):
            api_objects.cls_name_map_all

    def test_format_dt(self, api_objects):
        """Test datetime format works."""
        exp = datetime.datetime(2018, 12, 1, 23, 23, 10)
        try:
            assert api_objects.module_dt_format("2018-12-01T23:23:10") == exp
        except Exception:
            assert api_objects.module_dt_format("2018-12-01T23:23:10Z") == exp

    def test_item_by_name(self, api_objects):
        """Test get ApiItem by API name works."""
        cls = api_objects.cls_item_by_name("user")
        assert issubclass(cls, pytan3.api_models.ApiItem)
        assert issubclass(cls, pytan3.api_models.ApiModel)

    def test_item_by_name_bad(self, api_objects):
        """Test exc thrown on get ApiItem by invalid API name."""
        with pytest.raises(pytan3.api_objects.exceptions.UnknownApiNameError):
            api_objects.cls_item_by_name("badwolf")

    def test_list_by_name(self, api_objects):
        """Test get ApiList by API name works."""
        cls = api_objects.cls_list_by_name("users")
        assert issubclass(cls, pytan3.api_models.ApiList)
        assert issubclass(cls, pytan3.api_models.ApiModel)

    def test_list_by_name_bad(self, api_objects):
        """Test exc thrown on get ApiList by invalid API name."""
        with pytest.raises(pytan3.api_objects.exceptions.UnknownApiNameError):
            api_objects.cls_list_by_name("badwolf")

    def test_model_by_name(self, api_objects):
        """Test get ApiItem or ApiList by API name works."""
        cls = api_objects.cls_by_name("users")
        assert issubclass(cls, pytan3.api_models.ApiList)
        assert issubclass(cls, pytan3.api_models.ApiModel)
        cls = api_objects.cls_by_name("user")
        assert issubclass(cls, pytan3.api_models.ApiItem)
        assert issubclass(cls, pytan3.api_models.ApiModel)

    def test_model_by_name_bad(self, api_objects):
        """Test exc thrown on get ApiItem by invalid API name."""
        with pytest.raises(pytan3.api_objects.exceptions.UnknownApiNameError):
            api_objects.cls_by_name("badwolf")

    def test_auto_load(self, api_objects):
        """Test load works with defaults."""
        obj = api_objects.load()
        assert isinstance(obj, pytan3.api_objects.ApiObjects)

    def test_get_api(self, api_objects):
        """Test get_api_all* functions in modules."""
        assert isinstance(api_objects.module.get_api_all_item(), dict)
        assert isinstance(api_objects.module.get_api_all_list(), dict)
        assert isinstance(api_objects.module.get_api_all_model(), dict)

    def test_expand_glob_none_str(self, api_objects):
        """Test expand_global in modules."""
        obj = "None"
        exp = api_objects.module.expand_global(obj)
        assert exp is None

    def test_expand_glob_invalid_str(self, api_objects):
        """Test expand_global in modules."""
        obj = "badwolf"
        exp = api_objects.module.expand_global(obj)
        assert exp == "badwolf"

    def test_expand_glob_valid_str(self, api_objects):
        """Test expand_global in modules."""
        obj = "ApiList"
        exp = api_objects.module.expand_global(obj)
        assert issubclass(exp, pytan3.api_models.ApiList)

    def test_expand_glob_list(self, api_objects):
        """Test expand_global in modules."""
        obj = ["ApiList", "ApiItem", "badwolf"]
        exp = api_objects.module.expand_global(obj)
        assert issubclass(exp[0], pytan3.api_models.ApiList)
        assert issubclass(exp[1], pytan3.api_models.ApiItem)
        assert exp[2] == "badwolf"

    def test_expand_glob_dict(self, api_objects):
        """Test expand_global in modules."""
        obj = {"x": "ApiList", "y": "ApiItem", "z": "badwolf"}
        exp = api_objects.module.expand_global(obj)
        assert issubclass(exp["x"], pytan3.api_models.ApiList)
        assert issubclass(exp["y"], pytan3.api_models.ApiItem)
        assert exp["z"] == "badwolf"

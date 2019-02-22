# -*- coding: utf-8 -*-
"""Test suite for pytan3."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytan3
import pytest
import operator

string_types = pytan3.api_models.string_types
float_types = pytan3.api_models.float_types
integer_types = pytan3.api_models.integer_types


class TestApiObjectsLists(object):
    """Test ApiList object types."""

    @pytest.fixture
    def api_objects(self, api_module_any):
        """Fixture to get pytan3.api_objects.ApiObjects obj."""
        return pytan3.api_objects.ApiObjects(module_file=api_module_any["module_file"])

    def test_eq(self, api_objects):
        """Test __eq__."""
        cls = api_objects.UserList
        child_cls = api_objects.User
        obj1 = cls(child_cls(id=1), child_cls(id=2))
        obj2 = [child_cls(id=1), child_cls(id=2)]
        assert obj1 == obj2

    def test_attrs(self, api_objects):
        """Test all ApiLists have necessary API_ attrs."""
        for cls in api_objects.cls_list:
            assert issubclass(cls, pytan3.api_models.ApiModel)
            assert issubclass(cls, pytan3.api_models.ApiList)
            assert not issubclass(cls, pytan3.api_models.ApiItem)
            assert isinstance(cls.API_NAME, string_types)
            assert cls.API_NAME
            assert isinstance(cls.API_NAME_SRC, string_types)
            assert isinstance(cls.API_SIMPLE, dict)
            assert isinstance(cls.API_COMPLEX, dict)
            assert isinstance(cls.API_CONSTANTS, dict)
            assert isinstance(cls.API_STR, list)
            assert isinstance(cls.API_STR_ADD, list)
            assert isinstance(cls.API_ITEM_ATTR, string_types)
            if not isinstance(cls.API_ITEM_CLS, tuple):
                assert issubclass(cls.API_ITEM_CLS, pytan3.api_models.ApiModel)

    def test_str_repr(self, api_objects, monkeypatch):
        """Test obj with setattr has proper str/repr."""
        cls = api_objects.UserList
        monkeypatch.setitem(cls.API_SIMPLE, "name", string_types)
        child_cls = api_objects.User
        obj = cls()
        assert "UserList" in format(obj)
        assert "UserList" in repr(obj)
        assert "with 0 User objects" in format(obj)
        assert "user=[]" in repr(obj)
        obj.append(child_cls())
        assert "with 1 User objects" in format(obj)
        assert "id=None" in repr(obj)
        obj.append(child_cls(id=1))
        assert "with 2 User objects" in format(obj)
        assert "id=1" in repr(obj)
        obj.name = "x"
        assert "name={!r}".format("x") in format(obj)
        assert "name={!r}".format("x") in repr(obj)

    def test_str_repr_args(self, api_objects):
        """Test obj with args has proper str/repr."""
        cls = api_objects.UserList
        child_cls = api_objects.User
        obj = cls(child_cls(), child_cls(id=1))
        assert "with 2 User objects" in format(obj)
        assert "id=1" in repr(obj)

    def test_str_repr_args_list(self, api_objects):
        """Test obj with args as list expansion has proper str/repr."""
        cls = api_objects.UserList
        child_cls = api_objects.User
        obj = cls(*[child_cls(), child_cls(id=1)])
        assert "with 2 User objects" in format(obj)
        assert "id=1" in repr(obj)

    def test_str_repr_args_attr(self, api_objects):
        """Test obj with kwargs has proper str/repr with list attr=[]/()."""
        cls = api_objects.UserList
        child_cls = api_objects.User
        obj = cls(user=[child_cls(), child_cls(id=1)])
        assert "with 2 User objects" in format(obj)
        assert "id=1" in repr(obj)
        obj = cls(user=(child_cls(), child_cls(id=1)))
        assert "with 2 User objects" in format(obj)
        assert "id=1" in repr(obj)

    def test_instance_item(self, api_objects):
        """Test obj isinstance of ApiList."""
        cls = api_objects.UserList
        obj = cls()
        assert isinstance(obj, pytan3.api_models.ApiList)

    def test_str_coerce(self, api_objects, monkeypatch):
        """Test str coercion."""
        cls = api_objects.UserList
        monkeypatch.setitem(cls.API_SIMPLE, "name", string_types)
        obj = cls()
        obj.name = "abc"
        assert obj.name == "abc"
        obj.name = 123
        assert obj.name == "123"

    def test_str_coerce_kwargs(self, api_objects, monkeypatch):
        """Test str coercion via kwargs."""
        cls = api_objects.UserList
        monkeypatch.setitem(cls.API_SIMPLE, "name", string_types)
        obj = cls(name="abc")
        assert obj.name == "abc"
        obj = cls(name="123")

    def test_complex_on_simple_fail(self, api_objects, monkeypatch):
        """Test setattr complex on simple attr fails."""
        cls = api_objects.UserList
        monkeypatch.setitem(cls.API_SIMPLE, "name", string_types)
        obj = cls()
        with pytest.raises(pytan3.api_models.exceptions.AttrTypeError):
            obj.name = cls()
        with pytest.raises(pytan3.api_models.exceptions.AttrTypeError):
            obj.name = {}
        with pytest.raises(pytan3.api_models.exceptions.AttrTypeError):
            obj.name = []

    def test_complex_on_simple_fail_kwargs(self, api_objects, monkeypatch):
        """Test setattr complex on simple attr fails via kwargs."""
        cls = api_objects.UserList
        monkeypatch.setitem(cls.API_SIMPLE, "name", string_types)
        with pytest.raises(pytan3.api_models.exceptions.AttrTypeError):
            cls(name=cls())
        with pytest.raises(pytan3.api_models.exceptions.AttrTypeError):
            cls(name={})
        with pytest.raises(pytan3.api_models.exceptions.AttrTypeError):
            cls(name=[])

    def test_int_coerce(self, api_objects, monkeypatch):
        """Test int coercion."""
        cls = api_objects.UserList
        monkeypatch.setitem(cls.API_SIMPLE, "id", integer_types)
        obj = cls()
        obj.id = "1"
        assert obj.id == 1
        obj.id = 1
        assert obj.id == 1

    def test_int_coerce_kwargs(self, api_objects, monkeypatch):
        """Test int coercion via kwargs."""
        cls = api_objects.UserList
        monkeypatch.setitem(cls.API_SIMPLE, "id", integer_types)
        obj = cls(id="1")
        assert obj.id == 1
        obj = cls(id=1)
        assert obj.id == 1

    def test_int_bool_coerce(self, api_objects, monkeypatch):
        """Test bool to int coercion."""
        cls = api_objects.UserList
        monkeypatch.setitem(cls.API_SIMPLE, "id", integer_types)
        obj = cls()
        obj.id = True
        assert obj.id == 1

    def test_int_bool_coerce_kwargs(self, api_objects, monkeypatch):
        """Test bool to int coercion via kwargs."""
        cls = api_objects.UserList
        monkeypatch.setitem(cls.API_SIMPLE, "id", integer_types)
        obj = cls(id=True)
        assert obj.id == 1

    def test_int_coerce_fail(self, api_objects, monkeypatch):
        """Test exc thrown on invalid int."""
        cls = api_objects.UserList
        monkeypatch.setitem(cls.API_SIMPLE, "id", integer_types)
        obj = cls()
        with pytest.raises(pytan3.api_models.exceptions.AttrTypeError):
            obj.id = "abc"

    def test_none(self, api_objects, monkeypatch):
        """Test none works."""
        cls = api_objects.UserList
        monkeypatch.setitem(cls.API_SIMPLE, "id", integer_types)
        obj = cls()
        obj.id = None
        assert obj.id is None

    def test_none_kwargs(self, api_objects, monkeypatch):
        """Test none works via kwargs."""
        cls = api_objects.UserList
        monkeypatch.setitem(cls.API_SIMPLE, "id", integer_types)
        obj = cls(id=None)
        assert obj.id is None

    def test_undefined_attr_none_nowarnerror(self, api_objects):
        """Test setting undefined attr to None throws no warn or error."""
        cls = api_objects.UserList
        obj = cls()
        obj.non_existent_boo = None
        assert obj.non_existent_boo is None
        assert "non_existent_boo" not in obj.api_attrs()

    def test_undefined_attr_none_nowarnerror_kwargs(self, api_objects):
        """Test setting undefined attr to None throws no warn or error via kwargs."""
        cls = api_objects.UserList
        obj = cls(non_existent_boo=None)
        assert obj.non_existent_boo is None
        assert "non_existent_boo" not in obj.api_attrs()

    def test_float_coerce(self, api_objects, monkeypatch):
        """Test float coercion."""
        cls = api_objects.UserList
        monkeypatch.setitem(cls.API_SIMPLE, "floatilla", float_types)
        obj = cls()
        obj.floatilla = 0.3
        assert obj.floatilla == 0.3
        obj.floatilla = "0.3"
        assert obj.floatilla == 0.3

    def test_float_coerce_kwargs(self, api_objects, monkeypatch):
        """Test float coercion via kwargs."""
        cls = api_objects.UserList
        monkeypatch.setitem(cls.API_SIMPLE, "floatilla", float_types)
        obj = cls(floatilla=0.3)
        assert obj.floatilla == 0.3
        obj = cls(floatilla="0.3")
        assert obj.floatilla == 0.3

    def test_float_coerce_fail(self, api_objects, monkeypatch):
        """Test exc thrown on invalid float."""
        cls = api_objects.UserList
        monkeypatch.setitem(cls.API_SIMPLE, "floatilla", float_types)
        obj = cls()
        with pytest.raises(pytan3.api_models.exceptions.AttrTypeError):
            obj.floatilla = "abc"

    def test_unknown_complex_attr(self, api_objects):
        """Test exc thrown on unknown complex type."""
        cls = api_objects.UserList
        obj = cls()
        with pytest.raises(pytan3.api_models.exceptions.AttrUndefinedError):
            obj.moo = cls()
        with pytest.raises(pytan3.api_models.exceptions.AttrUndefinedError):
            obj.moo = {}
        with pytest.raises(pytan3.api_models.exceptions.AttrUndefinedError):
            obj.moo = []

    def test_append(self, api_objects):
        """Test append passthru to list container."""
        cls = api_objects.UserList
        child_cls = api_objects.User
        obj = cls()
        child_obj1 = child_cls(id=1)
        child_obj2 = child_cls(id=2)
        child_obj3 = child_cls(id=3)
        child_obj4 = {"id": 4}
        obj.append(child_obj1)
        obj.append(child_obj2)
        obj.append(child_obj3)
        obj.append(child_obj4)
        assert len(obj) == 4
        obj.remove(child_obj2)
        assert len(obj) == 3
        assert child_obj1 in obj
        assert child_obj2 not in obj
        assert child_obj3 in obj
        assert child_obj4 in obj

    def test_remove(self, api_objects):
        """Test remove passthru to list container."""
        cls = api_objects.UserList
        child_cls = api_objects.User
        child_obj1 = child_cls(id=1)
        child_obj2 = child_cls(id=2)
        child_obj3 = child_cls(id=3)
        child_obj4 = {"id": 4}
        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)
        assert len(obj) == 4
        obj.remove(child_obj2)
        assert len(obj) == 3
        assert child_obj1 in obj
        assert child_obj2 not in obj
        assert child_obj3 in obj
        assert child_obj4 in obj

    def test_pop(self, api_objects):
        """Test pop passthru to list container."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1)
        child_obj2 = child_cls(id=2)
        child_obj3 = child_cls(id=3)
        child_obj4 = {"id": 4}

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)
        assert len(obj) == 4

        pop1 = obj.pop()
        assert pop1 == child_obj4
        assert len(obj) == 3
        assert child_obj1 in obj
        assert child_obj2 in obj
        assert child_obj3 in obj
        assert child_obj4 not in obj

        pop2 = obj.pop(1)
        assert pop2 == child_obj2
        assert len(obj) == 2
        assert child_obj1 in obj
        assert child_obj2 not in obj
        assert child_obj3 in obj
        assert child_obj4 not in obj

    def test_reverse(self, api_objects):
        """Test reverse passthru to list container."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1)
        child_obj2 = child_cls(id=2)
        child_obj3 = child_cls(id=3)
        child_obj4 = {"id": 4}

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        assert obj[0].id == 1
        assert obj[1].id == 2
        assert obj[2].id == 3
        assert obj[3].id == 4
        obj.reverse()
        assert obj[0].id == 4
        assert obj[1].id == 3
        assert obj[2].id == 2
        assert obj[3].id == 1

    def test_get_item_by_attr(self, api_objects):
        """Test with defaults."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        get1 = obj.get_item_by_attr(value="boom4")
        assert get1 == child_obj4

    def test_get_item_by_attr_id(self, api_objects):
        """Test with id attr."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        get1 = obj.get_item_by_attr(value=3, attr="id")
        assert get1 == child_obj3

    def test_get_item_by_attr_nomatch(self, api_objects):
        """Test exc thrown when 0 items found."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        with pytest.raises(pytan3.api_models.exceptions.GetSingleItemError):
            obj.get_item_by_attr(value="boom5")

    def test_get_item_by_attr_nomatch_wrongtype(self, api_objects):
        """Test exc thrown when 0 items found due to wrong value type."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        with pytest.raises(pytan3.api_models.exceptions.GetSingleItemError):
            obj.get_item_by_attr(value=4)

    def test_get_item_by_attr_regex(self, api_objects):
        """Test regex value."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        get1 = obj.get_item_by_attr(value=".*4", regex_value=True)
        assert get1 == child_obj4

    def test_get_item_by_attr_regex_conv(self, api_objects):
        """Test regex value against int attr."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        get1 = obj.get_item_by_attr(value=".*4", attr="id", regex_value=True)
        assert get1 == child_obj4

    def test_get_item_by_attr_regex_toomany(self, api_objects):
        """Test exc thrown when more than 1 found with regex value."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        with pytest.raises(pytan3.api_models.exceptions.GetSingleItemError):
            obj.get_item_by_attr(value="boom.*", regex_value=True)

    def test_get_items_by_attr_1(self, api_objects):
        """Test finding 1 items."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        found = obj.get_items_by_attr(value="boom4")
        assert len(found) == 1
        assert found
        assert isinstance(found, list)
        assert found[0] == child_obj4

    def test_get_items_by_attr_0(self, api_objects):
        """Test finding 0 items."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        found = obj.get_items_by_attr(value="boom5")
        assert len(found) == 0
        assert not found
        assert isinstance(found, list)

    def test_get_items_by_attr_regex(self, api_objects):
        """Test finding many items via regex."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        found = obj.get_items_by_attr(value=r"boom[3-5]", regex_value=True)
        assert len(found) == 2
        assert found
        assert isinstance(found, list)
        assert found[0] == child_obj3
        assert found[1] == child_obj4

    def test_get_items_by_attr_regex_none(self, api_objects):
        """Test finding no items via regex."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        found = obj.get_items_by_attr(value=r"boom[5-9]", regex_value=True)
        assert len(found) == 0
        assert not found
        assert isinstance(found, list)

    def test_get_items_by_attr_regex_newlist_none(self, api_objects):
        """Test finding no items via regex with new list returned."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        found = obj.get_items_by_attr(
            value=r"boom[5-9]", regex_value=True, new_list=True
        )
        assert len(found) == 0
        assert not found
        assert isinstance(found, cls)

    def test_get_items_by_attr_regex_newlist_many(self, api_objects):
        """Test finding many items via regex with new list returned."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        found = obj.get_items_by_attr(
            value=r"boom[3-5]", regex_value=True, new_list=True
        )
        assert len(found) == 2
        assert found
        assert isinstance(found, cls)

    def test_pop_item_by_attr(self, api_objects):
        """Test with defaults."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        get1 = obj.pop_item_by_attr(value="boom4")
        assert get1 == child_obj4
        assert len(obj) == 3
        assert get1 not in obj

    def test_pop_item_by_attr_id(self, api_objects):
        """Test with id attr."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        get1 = obj.pop_item_by_attr(value=3, attr="id")
        assert get1 == child_obj3
        assert len(obj) == 3
        assert get1 not in obj

    def test_pop_item_by_attr_nomatch(self, api_objects):
        """Test exc thrown when 0 items found."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        with pytest.raises(pytan3.api_models.exceptions.GetSingleItemError):
            obj.pop_item_by_attr(value="boom5")

    def test_pop_item_by_attr_nomatch_wrongtype(self, api_objects):
        """Test exc thrown when 0 items found due to wrong value type."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        with pytest.raises(pytan3.api_models.exceptions.GetSingleItemError):
            obj.pop_item_by_attr(value=4)

    def test_pop_item_by_attr_regex(self, api_objects):
        """Test regex value."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        get1 = obj.pop_item_by_attr(value=".*4", regex_value=True)
        assert get1 == child_obj4
        assert len(obj) == 3
        assert get1 not in obj

    def test_pop_item_by_attr_regex_conv(self, api_objects):
        """Test regex value against int attr."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        get1 = obj.pop_item_by_attr(value=".*4", attr="id", regex_value=True)
        assert get1 == child_obj4
        assert len(obj) == 3
        assert get1 not in obj

    def test_pop_item_by_attr_regex_toomany(self, api_objects):
        """Test exc thrown when more than 1 found with regex value."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        with pytest.raises(pytan3.api_models.exceptions.GetSingleItemError):
            obj.pop_item_by_attr(value="boom.*", regex_value=True)

    def test_pop_items_by_attr_1(self, api_objects):
        """Test finding 1 items."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        found = obj.pop_items_by_attr(value="boom4")
        assert len(found) == 1
        assert found
        assert isinstance(found, list)
        assert found[0] == child_obj4
        assert len(obj) == 3
        assert found[0] not in obj

    def test_pop_items_by_attr_0(self, api_objects):
        """Test finding 0 items."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        found = obj.pop_items_by_attr(value="boom5")
        assert len(found) == 0
        assert not found
        assert isinstance(found, list)
        assert len(obj) == 4

    def test_pop_items_by_attr_regex(self, api_objects):
        """Test finding many items via regex."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        found = obj.pop_items_by_attr(value=r"boom[3-5]", regex_value=True)
        assert len(found) == 2
        assert found
        assert isinstance(found, list)
        assert found[0] == child_obj3
        assert found[1] == child_obj4
        assert len(obj) == 2
        assert found[0] not in obj
        assert found[1] not in obj

    def test_pop_items_by_attr_regex_none(self, api_objects):
        """Test finding no items via regex."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        found = obj.pop_items_by_attr(value=r"boom[5-9]", regex_value=True)
        assert len(found) == 0
        assert not found
        assert isinstance(found, list)
        assert len(obj) == 4

    def test_pop_items_by_attr_regex_newlist_none(self, api_objects):
        """Test finding no items via regex with new list returned."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        found = obj.pop_items_by_attr(
            value=r"boom[5-9]", regex_value=True, new_list=True
        )
        assert len(found) == 0
        assert not found
        assert isinstance(found, cls)
        assert len(obj) == 4

    def test_pop_items_by_attr_regex_newlist_many(self, api_objects):
        """Test finding many items via regex with new list returned."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="boom1")
        child_obj2 = child_cls(id=2, name="boom2")
        child_obj3 = child_cls(id=3, name="boom3")
        child_obj4 = child_cls(id=4, name="boom4")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)

        found = obj.pop_items_by_attr(
            value=r"boom[3-5]", regex_value=True, new_list=True
        )
        assert len(found) == 2
        assert found
        assert isinstance(found, cls)
        assert len(obj) == 2
        assert found[0] not in obj
        assert found[1] not in obj

    def test_sort_id(self, api_objects):
        """Test sort of default on id."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=7, name="abc1")
        child_obj2 = child_cls(id=4, name="mno")
        child_obj3 = child_cls(id=10, name="wxy")
        child_obj4 = child_cls(id=1, name="abc2")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)
        obj.sort()
        assert obj[0] == child_obj4
        assert obj[1] == child_obj2
        assert obj[2] == child_obj1
        assert obj[3] == child_obj3

    def test_sort_id_reverse(self, api_objects):
        """Test sort of default on id with reverse."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=7, name="abc1")
        child_obj2 = child_cls(id=4, name="mno")
        child_obj3 = child_cls(id=10, name="wxy")
        child_obj4 = child_cls(id=1, name="abc2")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)
        obj.sort(reverse=True)
        assert obj[3] == child_obj4
        assert obj[2] == child_obj2
        assert obj[1] == child_obj1
        assert obj[0] == child_obj3

    def test_sort_name(self, api_objects):
        """Test sort on name."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=7, name="abc1")
        child_obj2 = child_cls(id=4, name="mno")
        child_obj3 = child_cls(id=10, name="wxy")
        child_obj4 = child_cls(id=1, name="abc2")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)
        obj.sort(key=operator.attrgetter("name"))
        assert obj[0] == child_obj1
        assert obj[1] == child_obj4
        assert obj[2] == child_obj2
        assert obj[3] == child_obj3

    def test_sort_name_lambda(self, api_objects):
        """Test sort on name using lambda."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=7, name="abc1")
        child_obj2 = child_cls(id=4, name="mno")
        child_obj3 = child_cls(id=10, name="wxy")
        child_obj4 = child_cls(id=1, name="abc2")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)
        obj.sort(key=lambda x: x.name)
        assert obj[0] == child_obj1
        assert obj[1] == child_obj4
        assert obj[2] == child_obj2
        assert obj[3] == child_obj3

    def test_sort_name_lambda_reverse(self, api_objects):
        """Test sort on name using lambda with reverse."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=7, name="abc1")
        child_obj2 = child_cls(id=4, name="mno")
        child_obj3 = child_cls(id=10, name="wxy")
        child_obj4 = child_cls(id=1, name="abc2")

        obj = cls(child_obj1, child_obj2, child_obj3, child_obj4)
        obj.sort(key=lambda x: x.name, reverse=True)
        assert obj[3] == child_obj1
        assert obj[2] == child_obj4
        assert obj[1] == child_obj2
        assert obj[0] == child_obj3

    def test_init_attr_empty(self, api_objects):
        """Test init with empty value works."""
        cls = api_objects.UserList
        obj = cls(user=None)
        assert len(obj) == 0
        obj = cls()
        assert len(obj) == 0
        obj = cls(user=[])
        assert len(obj) == 0

    def test_init_attr_obj(self, api_objects):
        """Test init with child obj works."""
        cls = api_objects.UserList
        child_cls = api_objects.User
        obj = cls(user=child_cls(id=1))
        assert len(obj) == 1
        obj = cls(user=[child_cls(id=1), child_cls(id=2)])
        assert len(obj) == 2
        obj = cls(child_cls(id=1), child_cls(id=2))
        assert len(obj) == 2
        obj = cls({"id": 1}, {"id": 2})
        assert len(obj) == 2

    def test_contains_exc(self, api_objects):
        """Test no exc with "in" operator in invalid obj returns False ."""
        cls = api_objects.UserList

        obj = cls()
        assert {"x": {}} not in obj
        assert ([],) not in obj

    def test_add(self, api_objects):
        """Test + operator."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1)
        child_obj2 = child_cls(id=2)
        child_obj3 = {"id": 3}

        obj1 = cls(child_obj1, child_obj2)
        obj2 = cls(child_obj3)
        obj3 = obj1 + obj2

        assert isinstance(obj3, cls)

        assert len(obj1) == 2
        assert child_obj1 in obj1
        assert child_obj2 in obj1
        assert child_obj3 not in obj1

        assert len(obj2) == 1
        assert child_obj1 not in obj2
        assert child_obj2 not in obj2
        assert child_obj3 in obj2

        assert len(obj3) == 3
        assert child_obj1 in obj3
        assert child_obj2 in obj3
        assert child_obj3 in obj3

    def test_add_list(self, api_objects):
        """Test + operator using python list type."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1)
        child_obj2 = child_cls(id=2)
        child_obj3 = {"id": 3}

        obj1 = cls(child_obj1, child_obj2)
        obj2 = [child_obj3]
        obj3 = obj1 + obj2

        assert isinstance(obj3, cls)

        assert len(obj1) == 2
        assert child_obj1 in obj1
        assert child_obj2 in obj1
        assert child_obj3 not in obj1

        assert len(obj2) == 1
        assert child_obj1 not in obj2
        assert child_obj2 not in obj2
        assert child_obj3 in obj2

        assert len(obj3) == 3
        assert child_obj1 in obj3
        assert child_obj2 in obj3
        assert child_obj3 in obj3

    def test_add_empty(self, api_objects):
        """Test + operator with empty other value."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1)

        obj = cls(child_obj1) + None
        assert len(obj) == 1

        obj = cls(child_obj1) + []
        assert len(obj) == 1

        obj = cls(child_obj1) + cls()
        assert len(obj) == 1

    def test_add_bad(self, api_objects):
        """Test exc thrown with + operator against bad type."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        with pytest.raises(pytan3.api_models.exceptions.ListTypeError):
            cls(child_cls(id=1)) + child_cls()

    def test_iadd(self, api_objects):
        """Test += operator."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1)
        child_obj2 = child_cls(id=2)
        child_obj3 = {"id": 3}

        obj1 = cls(child_obj1, child_obj2)
        obj2 = cls(child_obj3)
        obj1 += obj2

        assert len(obj1) == 3
        assert child_obj1 in obj1
        assert child_obj2 in obj1
        assert child_obj3 in obj1

        assert len(obj2) == 1
        assert child_obj1 not in obj2
        assert child_obj2 not in obj2
        assert child_obj3 in obj2

    def test_iadd_list(self, api_objects):
        """Test += operator using python list type."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1)
        child_obj2 = child_cls(id=2)
        child_obj3 = {"id": 3}

        obj1 = cls(child_obj1, child_obj2)
        obj2 = [child_obj3]
        obj1 += obj2

        assert len(obj1) == 3
        assert child_obj1 in obj1
        assert child_obj2 in obj1
        assert child_obj3 in obj1

        assert len(obj2) == 1
        assert child_obj1 not in obj2
        assert child_obj2 not in obj2
        assert child_obj3 in obj2

    def test_iadd_empty(self, api_objects):
        """Test += operator with empty other value."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1)

        obj = cls(child_obj1)
        obj += None
        assert len(obj) == 1

        obj = cls(child_obj1)
        obj += []
        assert len(obj) == 1

        obj = cls(child_obj1)
        obj += cls()
        assert len(obj) == 1

    def test_iadd_bad(self, api_objects):
        """Test exc thrown with += operator against bad type."""
        cls = api_objects.UserList
        child_cls = api_objects.User
        obj = cls(child_cls(id=1))
        with pytest.raises(pytan3.api_models.exceptions.ListTypeError):
            obj += child_cls()

    def test_serialize(self, api_objects):
        """Test serialize."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="abc")
        obj = cls(child_obj1)

        item_dict = obj.serialize()
        assert item_dict == {"users": {"user": [{"id": 1, "name": "abc"}]}}

    def test_serialize_list_attrs_none(self, api_objects):
        """Test serialize with list attrs when object has no attrs."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="abc")
        obj = cls(child_obj1)

        item_dict = obj.serialize(list_attrs=True)
        assert item_dict == {"users": {"user": [{"id": 1, "name": "abc"}]}}

    def test_serialize_no_wrap(self, api_objects):
        """Test serialize without wrap_name."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="abc")
        obj = cls(child_obj1)

        item_dict = obj.serialize(wrap_name=False)
        assert item_dict == {"user": [{"id": 1, "name": "abc"}]}

    def test_serialize_no_wrap_item_attr(self, api_objects):
        """Test serialize without wrap_item_attr."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="abc")
        obj = cls(child_obj1)

        item_dict = obj.serialize(wrap_item_attr=False)
        assert item_dict == {"users": [{"id": 1, "name": "abc"}]}

    def test_serialize_no_wraps(self, api_objects):
        """Test serialize without any wraps."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        child_obj1 = child_cls(id=1, name="abc")
        obj = cls(child_obj1)

        item_dict = obj.serialize(wrap_name=False, wrap_item_attr=False)
        assert item_dict == [{"id": 1, "name": "abc"}]

    def test_serialize_exclude_attrs(self, api_objects, monkeypatch):
        """Test serialize without specific attrs."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        monkeypatch.setitem(cls.API_SIMPLE, "name", string_types)
        monkeypatch.setitem(cls.API_SIMPLE, "boo", string_types)

        child_obj1 = child_cls(id=1, name="abc")
        obj = cls(child_obj1, name="badwolf", boo="youare")

        item_dict = obj.serialize(exclude_attrs=["name"])
        assert item_dict == {"users": {"user": [{"id": 1}]}}

        item_dict = obj.serialize(exclude_attrs=["name"], list_attrs=True)
        assert item_dict == {"boo": "youare", "users": {"user": [{"id": 1}]}}

        item_dict = obj.serialize(exclude_attrs=["boo", "name"], list_attrs=True)
        assert item_dict == {"users": {"user": [{"id": 1}]}}

    def test_serialize_only_attrs(self, api_objects, monkeypatch):
        """Test serialize with only specific attrs."""
        cls = api_objects.UserList
        child_cls = api_objects.User

        monkeypatch.setitem(cls.API_SIMPLE, "name", string_types)
        monkeypatch.setitem(cls.API_SIMPLE, "boo", string_types)

        child_obj1 = child_cls(id=1, name="abc")
        obj = cls(child_obj1, name="badwolf", boo="youare")

        item_dict = obj.serialize(only_attrs=["name"])
        assert item_dict == {"users": {"user": [{"name": "abc"}]}}

        item_dict = obj.serialize(only_attrs=["name"], list_attrs=True)
        assert item_dict == {"name": "badwolf", "users": {"user": [{"name": "abc"}]}}

        item_dict = obj.serialize(only_attrs=["boo", "name"], list_attrs=True)
        assert item_dict == {
            "name": "badwolf",
            "boo": "youare",
            "users": {"user": [{"name": "abc"}]},
        }

    def test_check_item_int(self, api_objects):
        """Test list cls of int type works."""
        cls = api_objects.ComputerIdList
        obj = cls()
        obj.append(1)
        obj.append("2")
        assert 1 in obj
        assert 2 in obj

    def test_check_item_fail(self, api_objects):
        """Test exc thrown in list cls of int type with bad type."""
        cls = api_objects.ComputerIdList
        obj = cls()
        with pytest.raises(pytan3.api_models.exceptions.ListItemTypeError):
            obj.append("x")

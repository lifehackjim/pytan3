# -*- coding: utf-8 -*-
"""Test suite for pytan3."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytan3
import pytest
import copy

string_types = pytan3.api_models.string_types
float_types = pytan3.api_models.float_types
integer_types = pytan3.api_models.integer_types


class TestApiObjectsItems(object):
    """Test ApiItem object types."""

    @pytest.fixture
    def api_objects(self, api_module_any):
        """Fixture to get pytan3.api_objects.ApiObjects obj."""
        return pytan3.api_objects.ApiObjects(module_file=api_module_any["module_file"])

    def test_str_repr(self, api_objects):
        """Test obj setattr has proper str/repr."""
        cls = api_objects.User
        obj = cls()
        assert "User" in format(obj)
        assert "User" in repr(obj)

        assert "id=None" in format(obj)
        assert "id=None" in repr(obj)
        obj.id = 1
        assert "id=1" in format(obj)
        assert "id=1" in repr(obj)

        assert "locked_out=None" not in format(obj)
        assert "locked_out=None" in repr(obj)
        obj.locked_out = 1
        assert "locked_out=1" not in format(obj)
        assert "locked_out=1" in repr(obj)

    def test_attrs(self, api_objects):
        """Test all ApiItems have necessary API_ attrs."""
        for cls in api_objects.cls_item:
            assert issubclass(cls, pytan3.api_models.ApiModel)
            assert issubclass(cls, pytan3.api_models.ApiItem)
            assert not issubclass(cls, pytan3.api_models.ApiList)
            assert isinstance(cls.API_NAME, string_types)
            assert cls.API_NAME
            assert isinstance(cls.API_NAME_SRC, string_types)
            assert isinstance(cls.API_SIMPLE, dict)
            assert isinstance(cls.API_COMPLEX, dict)
            assert isinstance(cls.API_CONSTANTS, dict)
            assert isinstance(cls.API_STR, list)
            assert isinstance(cls.API_STR_ADD, list)
            assert isinstance(cls.API_LIST_API_NAME, string_types)
            if cls.API_LIST_CLS:
                assert issubclass(cls.API_LIST_CLS, pytan3.api_models.ApiList)

    def test_str_repr_kwargs(self, api_objects):
        """Test obj kwargs has proper str/repr."""
        cls = api_objects.User
        obj = cls(id=1, locked_out=1)
        assert "id=1" in format(obj)
        assert "id=1" in repr(obj)
        assert "locked_out=1" not in format(obj)
        assert "locked_out=1" in repr(obj)

    def test_instance_item(self, api_objects):
        """Test obj isinstance of ApiItem."""
        cls = api_objects.User
        obj = cls()
        assert isinstance(obj, pytan3.api_models.ApiItem)

    def test_str_coerce(self, api_objects):
        """Test str coercion."""
        cls = api_objects.User
        obj = cls()
        obj.name = "abc"
        assert obj.name == "abc"
        obj.name = 123
        assert obj.name == "123"

    def test_str_coerce_kwargs(self, api_objects):
        """Test str coercion via kwargs."""
        cls = api_objects.User
        obj = cls(name="abc")
        assert obj.name == "abc"
        obj = api_objects.User(name="123")

    def test_complex_on_simple_fail(self, api_objects):
        """Test setattr complex on simple attr fails."""
        cls = api_objects.User
        obj = cls()
        with pytest.raises(pytan3.api_models.exceptions.AttrTypeError):
            obj.name = cls()
        with pytest.raises(pytan3.api_models.exceptions.AttrTypeError):
            obj.name = {}
        with pytest.raises(pytan3.api_models.exceptions.AttrTypeError):
            obj.name = []

    def test_complex_on_simple_fail_kwargs(self, api_objects):
        """Test setattr complex on simple attr fails via kwargs."""
        cls = api_objects.User
        with pytest.raises(pytan3.api_models.exceptions.AttrTypeError):
            cls(name=cls())
        with pytest.raises(pytan3.api_models.exceptions.AttrTypeError):
            cls(name={})
        with pytest.raises(pytan3.api_models.exceptions.AttrTypeError):
            cls(name=[])

    def test_int_coerce(self, api_objects):
        """Test int coercion."""
        cls = api_objects.User
        obj = cls()
        obj.id = "1"
        assert obj.id == 1
        obj.id = 1
        assert obj.id == 1

    def test_int_coerce_kwargs(self, api_objects):
        """Test int coercion via kwargs."""
        cls = api_objects.User
        obj = cls(id="1")
        assert obj.id == 1
        obj = cls(id=1)
        assert obj.id == 1

    def test_int_bool_coerce(self, api_objects):
        """Test bool to int coercion."""
        cls = api_objects.User
        obj = cls()
        obj.id = True
        assert obj.id == 1

    def test_int_bool_coerce_kwargs(self, api_objects):
        """Test bool to int coercion via kwargs."""
        cls = api_objects.User
        obj = cls(id=True)
        assert obj.id == 1

    def test_int_coerce_fail(self, api_objects):
        """Test exc thrown on invalid int."""
        cls = api_objects.User
        obj = cls()
        with pytest.raises(pytan3.api_models.exceptions.AttrTypeError):
            obj.id = "abc"

    def test_none(self, api_objects):
        """Test none works."""
        cls = api_objects.User
        obj = cls()
        obj.id = None
        assert obj.id is None

    def test_none_kwargs(self, api_objects):
        """Test none works via kwargs."""
        cls = api_objects.User
        obj = cls(id=None)
        assert obj.id is None

    def test_undefined_attr_none_nowarnerror(self, api_objects):
        """Test setting undefined attr to None throws no warn or error."""
        cls = api_objects.User
        obj = cls()
        obj.non_existent_boo = None
        assert obj.non_existent_boo is None
        assert "non_existent_boo" not in obj.api_attrs()

    def test_undefined_attr_none_nowarnerror_kwargs(self, api_objects):
        """Test setting undefined attr to None throws no warn or error via kwargs."""
        cls = api_objects.User
        obj = cls(non_existent_boo=None)
        assert obj.non_existent_boo is None
        assert "non_existent_boo" not in obj.api_attrs()

    def test_float_coerce(self, api_objects, monkeypatch):
        """Test float coercion."""
        cls = api_objects.User
        monkeypatch.setitem(cls.API_SIMPLE, "floatilla", float_types)
        obj = cls()
        obj.floatilla = 0.3
        assert obj.floatilla == 0.3
        obj.floatilla = "0.3"
        assert obj.floatilla == 0.3

    def test_float_coerce_kwargs(self, api_objects, monkeypatch):
        """Test float coercion via kwargs."""
        cls = api_objects.User
        monkeypatch.setitem(cls.API_SIMPLE, "floatilla", float_types)
        obj = cls(floatilla=0.3)
        assert obj.floatilla == 0.3
        obj = cls(floatilla="0.3")
        assert obj.floatilla == 0.3

    def test_float_coerce_fail(self, api_objects, monkeypatch):
        """Test exc thrown on invalid float."""
        cls = api_objects.User
        monkeypatch.setitem(cls.API_SIMPLE, "floatilla", float_types)
        obj = cls()
        with pytest.raises(pytan3.api_models.exceptions.AttrTypeError):
            obj.floatilla = "abc"

    def test_copy(self, api_objects):
        """Test copy.copy works."""
        cls = api_objects.User
        child_cls1 = api_objects.UserRoleList
        child_cls2 = api_objects.UserRole
        obj1 = cls(id=1)
        obj1.roles = child_cls1()
        obj1.roles.append(child_cls2())
        obj2 = copy.copy(obj1)
        assert obj1 == obj2
        obj2.roles.append(child_cls2())
        assert obj1 == obj2
        obj2.id = 2
        assert obj1 != obj2

    def test_deepcopy(self, api_objects):
        """Test copy.deepcopy works."""
        cls = api_objects.User
        child_cls1 = api_objects.UserRoleList
        child_cls2 = api_objects.UserRole
        obj1 = cls(id=1)
        obj1.roles = child_cls1()
        obj1.roles.append(child_cls2())
        obj2 = copy.deepcopy(obj1)
        assert obj1 == obj2
        obj2.roles.append(child_cls2())
        assert obj1 != obj2

    def test_len(self, api_objects):
        """Test len on item is num of attrs set."""
        cls = api_objects.User
        child_cls = api_objects.UserRoleList
        obj = cls()
        assert len(obj) == 0
        assert not obj
        obj.id = 123
        assert len(obj) == 1
        assert obj
        obj.name = "badwolf"
        assert len(obj) == 2
        assert obj
        obj.roles = child_cls()
        assert len(obj) == 3
        assert obj

    def test_serialize(self, api_objects):
        """Test serialize."""
        cls = api_objects.User
        child_cls1 = api_objects.ContentSetRoleList
        child_cls2 = api_objects.ContentSetRole
        obj = cls()
        obj.id = 1
        obj.name = "abc"
        obj.content_set_roles = child_cls1()
        obj.content_set_roles.append(child_cls2(id=1, name="x", description="badwolf"))
        item_dict = obj.serialize()
        assert item_dict == {
            "user": {
                "id": 1,
                "name": "abc",
                "content_set_roles": {
                    "content_set_role": [
                        {"id": 1, "name": "x", "description": "badwolf"}
                    ]
                },
            }
        }

    def test_serialize_no_wrap_name(self, api_objects):
        """Test serialize without name wrap."""
        cls = api_objects.User
        child_cls1 = api_objects.ContentSetRoleList
        child_cls2 = api_objects.ContentSetRole
        obj = cls()
        obj.id = 1
        obj.name = "abc"
        obj.content_set_roles = child_cls1()
        obj.content_set_roles.append(child_cls2(id=1, name="x", description="badwolf"))
        item_dict = obj.serialize(wrap_name=False)
        assert item_dict == {
            "id": 1,
            "name": "abc",
            "content_set_roles": {
                "content_set_role": [{"id": 1, "name": "x", "description": "badwolf"}]
            },
        }

    def test_serialize_no_wrap_item_attr(self, api_objects):
        """Test serialize without item attr wrap."""
        cls = api_objects.User
        child_cls1 = api_objects.ContentSetRoleList
        child_cls2 = api_objects.ContentSetRole
        obj = cls()
        obj.id = 1
        obj.name = "abc"
        obj.content_set_roles = child_cls1()
        obj.content_set_roles.append(child_cls2(id=1, name="x", description="badwolf"))
        item_dict = obj.serialize(wrap_item_attr=False)
        assert item_dict == {
            "user": {
                "id": 1,
                "name": "abc",
                "content_set_roles": [{"id": 1, "name": "x", "description": "badwolf"}],
            }
        }

    def test_serialize_no_wraps(self, api_objects):
        """Test serialize without any wraps."""
        cls = api_objects.User
        child_cls1 = api_objects.ContentSetRoleList
        child_cls2 = api_objects.ContentSetRole
        obj = cls()
        obj.id = 1
        obj.name = "abc"
        obj.content_set_roles = child_cls1()
        obj.content_set_roles.append(child_cls2(id=1, name="x", description="badwolf"))
        item_dict = obj.serialize(wrap_name=False, wrap_item_attr=False)
        assert item_dict == {
            "id": 1,
            "name": "abc",
            "content_set_roles": [{"id": 1, "name": "x", "description": "badwolf"}],
        }

    def test_serialize_exclude_attrs(self, api_objects):
        """Test serialize without specific attrs."""
        cls = api_objects.User
        child_cls1 = api_objects.ContentSetRoleList
        child_cls2 = api_objects.ContentSetRole
        obj = cls()
        obj.id = 1
        obj.name = "abc"
        obj.content_set_roles = child_cls1()
        obj.content_set_roles.append(child_cls2(id=1, name="x", description="badwolf"))
        item_dict = obj.serialize(exclude_attrs=["name"])
        assert item_dict == {
            "user": {
                "id": 1,
                "content_set_roles": {
                    "content_set_role": [{"id": 1, "description": "badwolf"}]
                },
            }
        }

    def test_serialize_only_attrs(self, api_objects):
        """Test serialize with only specific attrs."""
        cls = api_objects.User
        obj = cls(id=1, name="abc")
        item_dict = obj.serialize(only_attrs=["id"])
        assert item_dict == {"user": {"id": 1}}

    def test_eq(self, api_objects):
        """Test __eq__."""
        cls = api_objects.User
        obj1 = cls(id=1)
        obj2 = cls(id=1)
        assert obj1 == obj2

    def test_neq(self, api_objects):
        """Test __neq__."""
        cls = api_objects.User
        obj1 = cls(id=1)
        obj2 = cls(id=2)
        obj3 = cls(id=1, name="moo")
        assert obj1 != obj2
        assert obj1 != obj3
        assert obj2 != obj3
        obj2.id = 1
        assert obj1 == obj2

    def test_complex_item_obj(self, api_objects, monkeypatch):
        """Test complex item=item obj."""
        cls = api_objects.User
        monkeypatch.setitem(cls.API_COMPLEX, "sub_user", cls)
        obj = cls()
        obj.sub_user = cls(id=1)
        assert isinstance(obj.sub_user, cls)
        assert obj.sub_user.id == 1

    def test_complex_item_obj_kwargs(self, api_objects, monkeypatch):
        """Test complex item attr=item obj via kwargs."""
        cls = api_objects.User
        monkeypatch.setitem(cls.API_COMPLEX, "sub_user", cls)
        obj = cls(sub_user=cls(id=1))
        assert isinstance(obj.sub_user, cls)
        assert obj.sub_user.id == 1

    def test_complex_item_coerce(self, api_objects, monkeypatch):
        """Test complex item attr=dict gets coerced."""
        cls = api_objects.User
        monkeypatch.setitem(cls.API_COMPLEX, "sub_user", cls)
        obj = cls()
        obj.sub_user = {"id": 1}
        assert isinstance(obj.sub_user, cls)
        assert obj.sub_user.id == 1

    def test_complex_item_coerce_kwargs(self, api_objects, monkeypatch):
        """Test complex item attr=dict via kwargs."""
        cls = api_objects.User
        monkeypatch.setitem(cls.API_COMPLEX, "sub_user", cls)
        obj = cls(sub_user={"id": 1})
        assert isinstance(obj.sub_user, cls)
        assert obj.sub_user.id == 1

    def test_complex_list_dict_list(self, api_objects):
        """Test complex list attr=list of dict."""
        cls = api_objects.Question
        child_cls1 = api_objects.SelectList
        child_cls2 = api_objects.Select
        obj = cls()
        obj.selects = [{"sensor": {"id": 1}}, {"sensor": {"id": 2}}]
        assert isinstance(obj.selects, child_cls1)
        assert isinstance(obj.selects[0], child_cls2)
        assert isinstance(obj.selects[1], child_cls2)
        assert obj.selects[0].sensor.id == 1
        assert obj.selects[1].sensor.id == 2
        assert len(obj) == 1
        assert len(obj.selects) == 2

    def test_unknown_simple_attr(self, api_objects):
        """Test warn on unknown simple attr."""
        cls = api_objects.User
        obj = cls()
        with pytest.warns(pytan3.api_models.exceptions.AttrUndefinedWarning) as r:
            obj.zoo1 = 123
            assert cls.API_SIMPLE["zoo1"] == integer_types
            assert "zoo1" in repr(obj)
            obj.zoo1 = 456
            assert len(r) == 1
        with pytest.warns(pytan3.api_models.exceptions.AttrUndefinedWarning) as r:
            obj.zoo2 = 0.3
            assert cls.API_SIMPLE["zoo2"] == float_types
            assert "zoo2" in repr(obj)
            obj.zoo2 = 0.4
            assert len(r) == 1
        with pytest.warns(pytan3.api_models.exceptions.AttrUndefinedWarning) as r:
            obj.zoo3 = "moo"
            assert cls.API_SIMPLE["zoo3"] == string_types
            assert "zoo3" in repr(obj)
            obj.zoo3 = "mike"
            assert len(r) == 1
        with pytest.warns(pytan3.api_models.exceptions.AttrUndefinedWarning) as r:
            obj.zoo4 = True
            assert cls.API_SIMPLE["zoo4"] == integer_types
            assert "zoo4" in repr(obj)
            obj.zoo4 = False
            obj.zoo4 = 56
            assert len(r) == 1

    def test_unknown_simple_attr_kwargs(self, api_objects, recwarn):
        """Test warn on unknown simple attr via kwargs."""
        cls = api_objects.User
        obj = cls()
        with pytest.warns(pytan3.api_models.exceptions.AttrUndefinedWarning) as r:
            obj = cls(meercat1=123)
            assert cls.API_SIMPLE["meercat1"] == integer_types
            assert "meercat1" in repr(obj)
            obj.meercat1 = 456
            assert len(r) == 1
        with pytest.warns(pytan3.api_models.exceptions.AttrUndefinedWarning) as r:
            obj = cls(meercat2=0.3)
            assert cls.API_SIMPLE["meercat2"] == float_types
            assert "meercat2" in repr(obj)
            obj.meercat2 = 0.6
            assert len(r) == 1
        with pytest.warns(pytan3.api_models.exceptions.AttrUndefinedWarning) as r:
            obj = cls(meercat3="moo")
            assert cls.API_SIMPLE["meercat3"] == string_types
            assert "meercat3" in repr(obj)
            obj.meercat3 = "meep"
            assert len(r) == 1
        with pytest.warns(pytan3.api_models.exceptions.AttrUndefinedWarning) as r:
            obj = cls(meercat4=True)
            assert cls.API_SIMPLE["meercat4"] == integer_types
            assert "meercat4" in repr(obj)
            obj.meercat4 = False
            obj.meercat4 = 56
            assert len(r) == 1

    def test_unknown_complex_attr(self, api_objects):
        """Test exc thrown on unknown complex type."""
        cls = api_objects.User
        obj = cls()
        with pytest.raises(pytan3.api_models.exceptions.AttrUndefinedError):
            obj.moo = cls()
        with pytest.raises(pytan3.api_models.exceptions.AttrUndefinedError):
            obj.moo = {}
        with pytest.raises(pytan3.api_models.exceptions.AttrUndefinedError):
            obj.moo = []

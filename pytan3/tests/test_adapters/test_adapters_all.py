# -*- coding: utf-8 -*-
"""Test suite for pytan3."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytan3
import pytest
import datetime

import six


def rng_name():
    """Generate random string for a username."""
    name = "b{dt.second}{dt.microsecond}"
    return name.format(dt=datetime.datetime.utcnow())


def test_load_invalid():
    """Test exc thrown on invalid object."""
    o = object()
    with pytest.raises(pytan3.adapters.exceptions.ModuleError):
        pytan3.adapters.load(o)


def test_load_type_invalid():
    """Test exc thrown on invalid string."""
    o = "bad"
    with pytest.raises(pytan3.adapters.exceptions.ModuleError):
        pytan3.adapters.load_type(o)


def test_load_type_rest():
    """Test load type rest works."""
    o = "rest"
    cls = pytan3.adapters.load_type(o)
    assert cls.get_type() == o
    assert issubclass(cls, pytan3.adapters.Adapter)


def test_load_type_soap():
    """Test load type soap works."""
    o = "soap"
    cls = pytan3.adapters.load_type(o)
    assert cls.get_type() == o
    assert issubclass(cls, pytan3.adapters.Adapter)


class TestAllAdapters(object):
    """Test adapters of any type."""

    @pytest.fixture
    def adapter(self, adapter_any, http_client, auth):
        """Get an adapter object of type: any."""
        api_module = adapter_any["api_module"]
        api_client_cls = adapter_any["api_client"]
        # adapter_cls = adapter_any["adapter"]
        adapter_cls = pytan3.adapters.load(adapter_any["adapter"])

        api_objects = pytan3.api_objects.ApiObjects(
            module_file=api_module["module_file"]
        )

        try:
            credentials_auth = pytan3.auth_methods.Credentials(
                http_client=http_client, **auth
            )
            api_client = api_client_cls(
                http_client=http_client, auth_method=credentials_auth
            )
            adapter = adapter_cls(api_client=api_client, api_objects=api_objects)
        except pytan3.utils.exceptions.VersionMismatchError as exc:  # pragma: no cover
            m = "Skipping due to version requirement failure: {e}".format(e=exc)
            pytest.skip(m)
        return adapter

    def test_api_objects_bad_version_min(self, adapter, monkeypatch):
        """Test exc thrown when ApiObjects does not meet min ver req for adapter."""
        api_objects = adapter.api_objects
        api_client = adapter.api_client
        adapter_cls = adapter.__class__

        version_req = {"vmin": "7.3.314.3409", "vmax": "", "veq": ""}
        monkeypatch.setattr(adapter_cls, "get_version_req", lambda x: version_req)

        monkeypatch.setattr(api_objects.module, "__version__", "7.1.1.1")
        monkeypatch.setattr(api_client, "_version", "7.3.314.3409", raising=False)

        with pytest.raises(pytan3.utils.exceptions.VersionMismatchError):
            adapter_cls(api_client=api_client, api_objects=api_objects)

    def test_api_objects_bad_version_max(self, adapter, monkeypatch):
        """Test exc thrown when ApiObjects does not meet max ver req for adapter."""
        api_objects = adapter.api_objects
        api_client = adapter.api_client
        adapter_cls = adapter.__class__

        version_req = {"vmin": "7.1.314.3409", "vmax": "7.0", "veq": ""}
        monkeypatch.setattr(adapter_cls, "get_version_req", lambda x: version_req)

        monkeypatch.setattr(api_objects.module, "__version__", "7.1.1.1")
        monkeypatch.setattr(api_client, "_version", "7.3.314.3409", raising=False)

        with pytest.raises(pytan3.utils.exceptions.VersionMismatchError):
            adapter_cls(api_client=api_client, api_objects=api_objects)

    def test_api_client_bad_version_min(self, adapter, monkeypatch):
        """Test exc thrown when ApiClient does not meet min ver req for adapter."""
        api_objects = adapter.api_objects
        api_client = adapter.api_client
        adapter_cls = adapter.__class__

        version_req = {"vmin": "7.3.314.3409", "vmax": "", "veq": ""}
        monkeypatch.setattr(adapter_cls, "get_version_req", lambda x: version_req)

        monkeypatch.setattr(api_client, "_version", "7.1.1.1", raising=False)

        with pytest.raises(pytan3.utils.exceptions.VersionMismatchError):
            adapter_cls(api_client=api_client, api_objects=api_objects)

    def test_api_client_bad_version_max(self, adapter, monkeypatch):
        """Test exc thrown when ApiClient does not meet max ver req for adapter."""
        api_objects = adapter.api_objects
        api_client = adapter.api_client
        adapter_cls = adapter.__class__

        version_req = {"vmin": "7.1.314.3409", "vmax": "7.0", "veq": ""}
        monkeypatch.setattr(adapter_cls, "get_version_req", lambda x: version_req)

        monkeypatch.setattr(api_client, "_version", "7.1.1.1", raising=False)

        with pytest.raises(pytan3.utils.exceptions.VersionMismatchError):
            adapter_cls(api_client=api_client, api_objects=api_objects)

    def test_objects_bad_type(self, adapter, monkeypatch):
        """Test exc thrown when bad type of ApiObjects used."""
        api_objects = adapter.api_objects
        api_client = adapter.api_client
        adapter_cls = adapter.__class__

        monkeypatch.setattr(api_objects.module, "TYPE", "badwolf")

        with pytest.raises(pytan3.adapters.exceptions.TypeMismatchError):
            adapter_cls(api_client=api_client, api_objects=api_objects)

    def test_api_client_bad_type(self, adapter, monkeypatch):
        """Test exc thrown when bad type of ApiClient used."""
        api_objects = adapter.api_objects
        api_client = adapter.api_client
        adapter_cls = adapter.__class__

        monkeypatch.setattr(api_client, "get_type", lambda: "badwolf")

        with pytest.raises(pytan3.adapters.exceptions.TypeMismatchError):
            adapter_cls(api_client=api_client, api_objects=api_objects)

    def test_pq(self, adapter):
        """Test parsed question text that is not canonical."""
        # parse the question text into parsed result groups
        q = "Get Computer Namex and IP Addressx from all machines"
        result1 = adapter.api_parse_question(q)
        parse_obj = result1()
        assert isinstance(result1, pytan3.results.Result)
        assert len(parse_obj) > 1

        # ensure the first parsed group says it is NOT a canonical match
        if result1.api_objects.module_type == "rest":
            assert isinstance(parse_obj, adapter.api_objects.ParseQuestionResultList)
            assert isinstance(parse_obj[0], adapter.api_objects.ParseQuestionResult)
            assert parse_obj[0].from_canonical_text == 0
        else:
            assert isinstance(parse_obj, adapter.api_objects.ParseResultGroupList)
            assert isinstance(parse_obj[0], adapter.api_objects.ParseResultGroup)
            assert parse_obj[0].question.from_canonical_text == 0
        return parse_obj

    @pytest.fixture
    def test_pq_canon(self, adapter):
        """Test parsed question text that is canonical."""
        # parse the question text into parsed result groups
        q = "Get Computer Name and IP Address from all machines"
        result1 = adapter.api_parse_question(q)
        parse_obj = result1()
        assert isinstance(result1, pytan3.results.Result)
        assert len(parse_obj) == 1

        # ensure the first parsed group says it IS a canonical match
        # SOAP and REST API's for this largely work the same, with some differences.
        if result1.api_objects.module_type == "rest":
            assert isinstance(parse_obj, adapter.api_objects.ParseQuestionResultList)
            assert isinstance(parse_obj[0], adapter.api_objects.ParseQuestionResult)
            assert parse_obj[0].from_canonical_text == 1
        else:
            assert isinstance(parse_obj, adapter.api_objects.ParseResultGroupList)
            assert isinstance(parse_obj[0], adapter.api_objects.ParseResultGroup)
            assert parse_obj[0].question.from_canonical_text == 1

        return parse_obj

    @pytest.fixture
    def test_pq_canon_ask(self, adapter, test_pq_canon):
        """Test asking parsed question that is canonical."""
        parse_obj = test_pq_canon

        # add the first parsed group as a question
        result1 = adapter.api_add_parsed_question(parse_obj[0])
        added_question_obj = result1()
        assert isinstance(result1, pytan3.results.Result)
        assert isinstance(added_question_obj, adapter.api_objects.Question)
        assert not added_question_obj.query_text

        # refetch the added question to get the full object
        result2 = adapter.api_get(added_question_obj)
        question_obj = result2()
        assert isinstance(result2, pytan3.results.Result)
        assert isinstance(question_obj, adapter.api_objects.Question)
        assert question_obj.query_text
        return question_obj

    def test_pq_canon_get_ri(self, adapter, test_pq_canon_ask):
        """Test get_result_info for parsed question that is canonical."""
        question_obj = test_pq_canon_ask

        # get the result info for the added question
        result = adapter.api_get_result_info(question_obj)
        assert isinstance(result.api_objects, pytan3.api_objects.ApiObjects)
        assert isinstance(result.url, six.string_types)
        assert isinstance(result.status_code, six.integer_types)
        assert isinstance(result.method, six.string_types)
        assert isinstance(result.request_body_str, six.string_types)
        assert isinstance(result.request_body_obj, (list, dict))
        assert isinstance(result.request_object_obj, (list, dict))
        assert isinstance(result.response_body_str, six.string_types)
        assert isinstance(result.response_body_obj, (list, dict))
        with pytest.raises(pytan3.results.exceptions.ApiWrongRequestType):
            result.object_api()
        assert hasattr(result, "object_obj")
        assert isinstance(result.object_obj, dict)

        ri_manual = result.data_api()
        ri_obj = result()
        assert ri_manual == ri_obj
        assert format(ri_obj) == repr(ri_obj)
        assert isinstance(result, pytan3.results.Result)
        assert isinstance(ri_obj, adapter.api_objects.ResultInfoList)
        assert len(ri_obj) == 1
        assert isinstance(ri_obj[0], adapter.api_objects.ResultInfo)
        assert format(ri_obj[0]) == repr(ri_obj[0])

    def test_pq_canon_get_rd(self, adapter, test_pq_canon_ask):
        """Test get_result_data for parsed question that is canonical."""
        question_obj = test_pq_canon_ask

        # get the result data for the added question
        result1 = adapter.api_get_result_data(question_obj)
        rd_obj = result1()
        assert isinstance(result1, pytan3.results.Result)
        assert isinstance(rd_obj, adapter.api_objects.ResultSetList)
        assert len(rd_obj) == 1
        assert isinstance(rd_obj[0], adapter.api_objects.ResultSet)

    def test_pq_canon_get_mrd(self, adapter, test_pq_canon_ask):
        """Test get_merged_result_data for parsed question that is canonical."""
        question_obj = test_pq_canon_ask
        # get the merged result data for the added question
        result1 = adapter.api_get_merged_result_data([question_obj])
        mrd_obj = result1()
        assert isinstance(result1, pytan3.results.Result)
        assert isinstance(mrd_obj, adapter.api_objects.MergedResultSet)
        assert isinstance(mrd_obj.result_infos, adapter.api_objects.ResultInfoList)
        assert len(mrd_obj.result_infos) == 1
        assert isinstance(mrd_obj.result_sets, adapter.api_objects.ResultSetList)
        assert len(mrd_obj.result_sets) == 1

    def test_get_client_count(self, adapter):
        """Test get_client_count works."""
        result = adapter.api_get_client_count()
        obj = result()
        assert isinstance(result, pytan3.results.Result)
        assert isinstance(obj, adapter.api_objects.ClientCount)
        assert isinstance(obj.count, six.integer_types)

    def test_get_user_list(self, adapter):
        """Test api_get works w/ user list obj to get all users."""
        find = adapter.api_objects.UserList()
        result = adapter.api_get(find)
        obj = result()
        assert isinstance(result, pytan3.results.Result)
        assert isinstance(obj, adapter.api_objects.UserList)
        assert len(obj) >= 1
        assert isinstance(obj[0], adapter.api_objects.User)

    @pytest.fixture
    def user_result(self, adapter):
        """Get result from get user valid user id."""
        find_user = adapter.api_objects.User(id=adapter.api_client.auth_method.uid)
        result = adapter.api_get(find_user)
        return result

    def test_get_user(self, adapter, user_result):
        """Test user result with valid user id."""
        user_manual = user_result.object_api()
        user = user_result()
        assert user_manual == user
        assert isinstance(user_result, pytan3.results.Result)
        assert isinstance(user, adapter.api_objects.User)
        assert user.id == adapter.api_client.auth_method.uid

    def test_object_data_badtype(self, adapter, user_result):
        """Test exc thrown when get data api in get object req."""
        with pytest.raises(pytan3.results.exceptions.ApiWrongRequestType):
            user_result.data_api()

    def test_data_object_badtype(self, adapter, test_pq_canon_ask):
        """Test exc thrown when get object api in get data req."""
        question_obj = test_pq_canon_ask

        # get the result data for the added question
        result = adapter.api_get_result_data(question_obj)
        with pytest.raises(pytan3.results.exceptions.ApiWrongRequestType):
            result.object_api()

    def test_result_props(self, adapter, user_result):
        """Test result properties."""
        assert "method=" in format(user_result)
        assert "method=" in repr(user_result)
        assert hasattr(user_result, "__call__")
        assert hasattr(user_result, "from_response")
        assert hasattr(user_result, "error_check")
        assert hasattr(user_result, "error_text")
        assert hasattr(user_result, "data_obj")
        assert isinstance(user_result.api_objects, pytan3.api_objects.ApiObjects)
        assert isinstance(user_result.url, six.string_types)
        assert isinstance(user_result.status_code, six.integer_types)
        assert isinstance(user_result.method, six.string_types)
        assert isinstance(user_result.request_body_str, six.string_types)
        assert isinstance(user_result.request_body_obj, (list, dict))
        assert isinstance(user_result.request_object_obj, (list, dict))
        assert isinstance(user_result.response_body_str, six.string_types)
        assert isinstance(user_result.response_body_obj, (list, dict))

    def test_result_get_dict_path_bad(self, adapter, user_result):
        """Test exc thrown with bad dict path."""
        with pytest.raises(pytan3.results.exceptions.DictionaryPathError):
            user_result.get_dict_path(obj={"x": "y"}, path="/x/x", src="badwolf")

    def test_get_user_invalid(self, adapter):
        """Test exc thrown in api_get w/ invalid user id."""
        find_user = adapter.api_objects.User(id=99999999999)
        result = adapter.api_get(find_user)
        assert isinstance(result, pytan3.results.Result)
        with pytest.raises(pytan3.results.exceptions.ObjectNotFoundError):
            result()

    def test_get_badtype(self, adapter):
        """Test exc thrown in api_get w/ invalid type."""
        with pytest.raises(pytan3.adapters.exceptions.InvalidTypeError):
            adapter.api_get("")

    def test_add_badtype(self, adapter):
        """Test exc thrown in api_add w/ invalid type."""
        with pytest.raises(pytan3.adapters.exceptions.InvalidTypeError):
            adapter.api_add(adapter.api_objects.UserList())

    def test_update_missing_attrs(self, adapter):
        """Test exc thrown in api_update w/ user with no attrs set."""
        with pytest.raises(pytan3.adapters.exceptions.EmptyAttributeError):
            adapter.api_update(adapter.api_objects.User())

    def test_get_result_info_missing_attrs(self, adapter):
        """Test exc thrown in api_get_result_info w/ question with no attrs set."""
        with pytest.raises(pytan3.adapters.exceptions.EmptyAttributeError):
            adapter.api_get_result_info(adapter.api_objects.Question())

    def test_get_result_data_missing_attrs(self, adapter):
        """Test exc thrown in api_get_result_data w/ question with no attrs set."""
        with pytest.raises(pytan3.adapters.exceptions.EmptyAttributeError):
            adapter.api_get_result_data(adapter.api_objects.Question())

    def test_delete_missing_attrs(self, adapter):
        """Test exc thrown in api_delete w/ user with no attrs set."""
        with pytest.raises(pytan3.adapters.exceptions.EmptyAttributeError):
            adapter.api_delete(adapter.api_objects.User())

    def test_update_bad_listtype(self, adapter):
        """Test exc thrown in api_update w/ ApiList object."""
        with pytest.raises(pytan3.adapters.exceptions.InvalidTypeError):
            adapter.api_update(adapter.api_objects.UserList())

    def test_delete_bad_listtype(self, adapter):
        """Test exc thrown in api_delete w/ ApiList object."""
        with pytest.raises(pytan3.adapters.exceptions.InvalidTypeError):
            adapter.api_delete(adapter.api_objects.UserList())

    def test_get_audit_logs_badtype(self, adapter):
        """Test exc thrown in api_get_audit_logs w/ bad type."""
        with pytest.raises(pytan3.adapters.exceptions.InvalidTypeError):
            adapter.api_get_audit_logs(type="moo", target=1)

    @pytest.fixture
    def test_user_add(self, adapter):
        """Test api_add works to add a new user."""
        name = rng_name()
        try:
            add_user = adapter.api_objects.User(name=name)
        except pytan3.results.exceptions.ObjectExistsError:  # pragma: no cover
            name = rng_name()
            add_user = adapter.api_objects.User(name=name)

        result = adapter.api_add(add_user)
        obj = result()
        assert isinstance(result, pytan3.results.Result)
        assert isinstance(obj, adapter.api_objects.User)
        assert obj.name == name
        assert obj.deleted_flag == 0
        return obj

    @pytest.fixture
    def test_user_get_added(self, adapter, test_user_add):
        """Test api_get works to against newly added user."""
        find_obj = test_user_add
        result = adapter.api_get(find_obj)
        obj = result()
        assert isinstance(result, pytan3.results.Result)
        assert isinstance(obj, adapter.api_objects.User)
        assert obj == find_obj
        assert obj.name == find_obj.name
        assert obj.deleted_flag == 0
        return obj

    @pytest.fixture
    def test_user_update_added(self, adapter, test_user_get_added):
        """Test api_get works to against newly added user."""
        original_obj = test_user_get_added
        update_obj = adapter.api_objects.User(**original_obj.serialize(wrap_name=False))
        update_obj.display_name = "badwolf"
        result = adapter.api_update(update_obj)
        obj = result()
        assert isinstance(result, pytan3.results.Result)
        assert isinstance(obj, adapter.api_objects.User)
        assert obj != original_obj
        assert obj.name == original_obj.name
        assert obj.id == original_obj.id
        assert obj.display_name == "badwolf"
        assert obj.deleted_flag == 0
        return obj

    def test_user_delete_added_and_updated(self, adapter, test_user_update_added):
        """Test api_get works to against newly added and updated user."""
        delete_obj = test_user_update_added
        result = adapter.api_delete(delete_obj)
        obj = result()
        assert isinstance(result, pytan3.results.Result)
        assert isinstance(obj, adapter.api_objects.User)
        assert obj != delete_obj
        assert obj.name == delete_obj.name
        assert obj.id == delete_obj.id
        assert obj.deleted_flag == 1

    def test_bad_status_code(self, adapter):
        """Test exc thrown with bad status code."""
        result = adapter.api_get(adapter.api_objects.User(id=adapter.auth_method.uid))
        result._status_code = 500
        with pytest.raises(pytan3.results.exceptions.ResponseError):
            result()

    def test_str_parse_error(self, adapter, user_result):
        """Test exc thrown with str to obj parse."""
        with pytest.raises(pytan3.results.exceptions.TextDeserializeError):
            user_result.str_to_obj(text="<>", src="badwolf")

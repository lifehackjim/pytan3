# -*- coding: utf-8 -*-
"""Test suite for pytan3."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytan3
import pytest
import six

from .data_sets import data_sets


class TestComputerName(object):
    """Test ResultSet for all API Object modules.

    Question: "Get Computer Name from all machines"
    """

    @pytest.fixture
    def api_objects(self, api_module_any):
        """Fixture to get a pytan3.api_objects.ApiObjects of type SOAP."""
        return pytan3.api_objects.ApiObjects(module_file=api_module_any["module_file"])

    @pytest.fixture
    def data(self, api_objects):
        """Fixture to load result set from JSON data file."""
        api_type = api_objects.module_type
        datas_dict = data_sets[api_type]["data_name"]
        datas = api_objects.ResultSetList(**datas_dict)
        assert len(datas) == 1
        data = datas[0]
        assert isinstance(data, api_objects.ResultSet)
        assert data.select_count == 1
        return data

    def test_cols(self, api_objects, data):
        """Test columns attr."""
        assert isinstance(data.columns, api_objects.ColumnList)
        assert len(data.columns) == 2
        assert data.columns.names == ["Computer Name", "Count"]
        assert repr(data.columns) == format(data.columns)

    def test_col_properties(self, api_objects, data):
        """Test column properties."""
        assert data.columns[0].name == "Computer Name"
        assert data.columns[0].type == 1
        assert data.columns[0].result_type == "TEXT_RESULT"
        assert data.columns[0].hash == 3409330187
        assert data.columns[0].API_DATA_SET == data
        assert data.columns[0].API_IDX == 0
        assert data.columns[1].name == "Count"
        assert data.columns[1].type == 3
        assert data.columns[1].result_type == "NUMERIC_RESULT"
        assert data.columns[1].hash == 0
        assert data.columns[1].API_DATA_SET == data
        assert data.columns[1].API_IDX == 1

    def test_col_idx(self, api_objects, data):
        """Test string indexing maps to same int index."""
        assert data.columns[0] == data.columns["Computer Name"]
        assert data.columns[1] == data.columns["Count"]

    def test_col_idx_bad(self, api_objects, data):
        """Test exc thrown on bad str index."""
        with pytest.raises(pytan3.api_objects.exceptions.ModuleError):
            data.columns["Nope"]

    def test_col_get_values(self, api_objects, data):
        """Test getting values from all rows for each column."""
        exp = [["batgirl"], ["aquaman"], ["cyborg"], ["metallo"]]
        assert data.columns[0].get_values() == exp
        exp = [["1"], ["1"], ["1"], ["1"]]
        assert data.columns[1].get_values() == exp

    def test_col_get_values_join(self, api_objects, data):
        """Test getting values from all rows for each column with a join str."""
        exp = ["batgirl", "aquaman", "cyborg", "metallo"]
        assert data.columns[0].get_values(join="\n") == exp
        exp = ["1", "1", "1", "1"]
        assert data.columns[1].get_values(join="\n") == exp

    def test_rows(self, api_objects, data):
        """Test rows attr."""
        assert isinstance(data.rows, api_objects.RowList)
        assert len(data.rows) == 4
        assert repr(data.rows) == format(data.rows)

    def test_row_properties(self, api_objects, data):
        """Test row properties."""
        for row in data.rows:
            assert isinstance(row, api_objects.Row)
            assert isinstance(row.id, six.integer_types)
            assert isinstance(row.cid, six.integer_types)
            assert isinstance(row.columns, api_objects.RowColumnList)
            assert repr(row) == format(row)
            assert row.names == ["Computer Name", "Count"]
            assert len(row) == 2
            for column in row:
                assert isinstance(column, api_objects.RowColumn)
                assert isinstance(column.API_COLUMN, api_objects.Column)
                assert column.API_IDX == column.API_COLUMN.API_IDX
                for value in column:
                    assert isinstance(value, api_objects.RowValue)
                    assert isinstance(value.hash, (type(None), six.integer_types))
                    assert isinstance(value.value, six.string_types)

    def test_row_idx(self, api_objects, data):
        """Test string indexing maps to same int index."""
        for row in data.rows:
            assert row[0] == row["Computer Name"]
            assert row[1] == row["Count"]

    def test_row_idx_bad(self, api_objects, data):
        """Test exc thrown on bad str index."""
        for row in data.rows:
            with pytest.raises(pytan3.api_objects.exceptions.ModuleError):
                row["Nope"]

    def test_row_get_values(self, api_objects, data):
        """Test getting values for each row."""
        exp = {"Computer Name": ["batgirl"], "Count": ["1"]}
        assert data.rows[0].get_values() == exp

        exp = {"Computer Name": ["aquaman"], "Count": ["1"]}
        assert data.rows[1].get_values() == exp

        exp = {"Computer Name": ["cyborg"], "Count": ["1"]}
        assert data.rows[2].get_values() == exp

        exp = {"Computer Name": ["metallo"], "Count": ["1"]}
        assert data.rows[3].get_values() == exp

    def test_row_get_values_join(self, api_objects, data):
        """Test getting values for each row with a join str."""
        exp = {"Computer Name": "batgirl", "Count": "1"}
        assert data.rows[0].get_values(join="\n") == exp

        exp = {"Computer Name": "aquaman", "Count": "1"}
        assert data.rows[1].get_values(join="\n") == exp

        exp = {"Computer Name": "cyborg", "Count": "1"}
        assert data.rows[2].get_values(join="\n") == exp

        exp = {"Computer Name": "metallo", "Count": "1"}
        assert data.rows[3].get_values(join="\n") == exp

    def test_row_get_values_join_meta_hashes(self, api_objects, data):
        """Test getting values for each row with meta, hashes, and a join str."""
        exp = {
            "Computer Name": "batgirl",
            "Computer Name Hash Values": "1163752210",
            "Computer Name Sensor Hash": 3409330187,
            "Computer Name Result Type": "TEXT_RESULT",
            "Count": "1",
            "Count Hash Values": "",
            "Count Sensor Hash": 0,
            "Count Result Type": "NUMERIC_RESULT",
        }
        assert data.rows[0].get_values(meta=True, hashes=True, join="\n") == exp
        exp = {
            "Computer Name": "aquaman",
            "Computer Name Hash Values": "1655949567",
            "Computer Name Sensor Hash": 3409330187,
            "Computer Name Result Type": "TEXT_RESULT",
            "Count": "1",
            "Count Hash Values": "",
            "Count Sensor Hash": 0,
            "Count Result Type": "NUMERIC_RESULT",
        }
        assert data.rows[1].get_values(meta=True, hashes=True, join="\n") == exp
        exp = {
            "Computer Name": "cyborg",
            "Computer Name Hash Values": "2779630309",
            "Computer Name Sensor Hash": 3409330187,
            "Computer Name Result Type": "TEXT_RESULT",
            "Count": "1",
            "Count Hash Values": "",
            "Count Sensor Hash": 0,
            "Count Result Type": "NUMERIC_RESULT",
        }
        assert data.rows[2].get_values(meta=True, hashes=True, join="\n") == exp
        exp = {
            "Computer Name": "metallo",
            "Computer Name Hash Values": "3744311725",
            "Computer Name Sensor Hash": 3409330187,
            "Computer Name Result Type": "TEXT_RESULT",
            "Count": "1",
            "Count Hash Values": "",
            "Count Sensor Hash": 0,
            "Count Result Type": "NUMERIC_RESULT",
        }
        assert data.rows[3].get_values(meta=True, hashes=True, join="\n") == exp


class TestComputerNameIpAddress(object):
    """Test ResultSet for all API Object modules.

    Question: "Get Computer Name and IP Address from all machines"
    """

    @pytest.fixture
    def api_objects(self, api_module_any):
        """Fixture to get a pytan3.api_objects.ApiObjects of type SOAP."""
        return pytan3.api_objects.ApiObjects(module_file=api_module_any["module_file"])

    @pytest.fixture
    def data(self, api_objects):
        """Fixture to load result set from JSON data file."""
        api_type = api_objects.module_type
        datas_dict = data_sets[api_type]["data_name_ip"]
        datas = api_objects.ResultSetList(**datas_dict)
        assert len(datas) == 1
        data = datas[0]
        assert isinstance(data, api_objects.ResultSet)
        assert data.select_count == 2
        return data

    def test_cols(self, api_objects, data):
        """Test columns attr."""
        assert isinstance(data.columns, api_objects.ColumnList)
        assert len(data.columns) == 3
        assert data.columns.names == ["Computer Name", "IP Address", "Count"]
        assert repr(data.columns) == format(data.columns)

    def test_rows(self, api_objects, data):
        """Test rows attr."""
        assert isinstance(data.rows, api_objects.RowList)
        assert len(data.rows) >= 1
        assert repr(data.rows) == format(data.rows)

    def test_row_get_values(self, api_objects, data):
        """Test getting values for each row."""
        for row in data.rows:
            values = row.get_values()
            assert isinstance(values, dict)
            for column in data.columns:
                assert column.name in values
                assert isinstance(values[column.name], list)

    def test_row_get_values_join(self, api_objects, data):
        """Test getting values for each row with a join str."""
        for row in data.rows:
            values = row.get_values(join="\n")
            assert isinstance(values, dict)
            for column in data.columns:
                assert column.name in values
                assert isinstance(values[column.name], six.string_types)

    def test_row_get_values_join_meta_hashes(self, api_objects, data):
        """Test getting values for each row with meta, hashes, and a join str."""
        for row in data.rows:
            values = row.get_values(meta=True, hashes=True, join="\n")
            assert isinstance(values, dict)
            for column in data.columns:
                assert column.name in values
                assert isinstance(values[column.name], six.string_types)


class TestComputerNameIpAddressIpRoute(object):
    """Test ResultSet for all API Object modules.

    Question: "Get Computer Name and IP Address and IP Route Details from all machines"
    """

    @pytest.fixture
    def api_objects(self, api_module_any):
        """Fixture to get a pytan3.api_objects.ApiObjects of type SOAP."""
        return pytan3.api_objects.ApiObjects(module_file=api_module_any["module_file"])

    @pytest.fixture
    def data(self, api_objects):
        """Fixture to load result set from JSON data file."""
        api_type = api_objects.module_type
        datas_dict = data_sets[api_type]["data_name_ip_iproute"]
        datas = api_objects.ResultSetList(**datas_dict)
        assert len(datas) == 1
        data = datas[0]
        assert isinstance(data, api_objects.ResultSet)
        assert data.select_count == 3
        return data

    def test_col_idx(self, api_objects, data):
        """Test string indexing maps to same int index."""
        assert data.columns[0] == data.columns["Computer Name"]
        assert data.columns[8] == data.columns["Count"]

    def test_col_idx_bad(self, api_objects, data):
        """Test exc thrown on bad str index."""
        with pytest.raises(pytan3.api_objects.exceptions.ModuleError):
            data.columns["Nope"]

    def test_cols(self, api_objects, data):
        """Test columns attr."""
        assert isinstance(data.columns, api_objects.ColumnList)
        assert len(data.columns) == 9
        assert data.columns.names == [
            "Computer Name",
            "IP Address",
            "Destination",
            "Gateway",
            "Mask",
            "Flags",
            "Metric",
            "Interface",
            "Count",
        ]
        assert repr(data.columns) == format(data.columns)

    def test_rows(self, api_objects, data):
        """Test rows attr."""
        assert isinstance(data.rows, api_objects.RowList)
        assert len(data.rows) >= 1
        assert repr(data.rows) == format(data.rows)

    def test_row_get_values(self, api_objects, data):
        """Test getting values for each row."""
        for row in data.rows:
            values = row.get_values()
            assert isinstance(values, dict)
            for column in data.columns:
                assert column.name in values
                assert isinstance(values[column.name], list)

    def test_row_get_values_join(self, api_objects, data):
        """Test getting values for each row with a join str."""
        for row in data.rows:
            values = row.get_values(join="\n")
            assert isinstance(values, dict)
            for column in data.columns:
                assert column.name in values
                assert isinstance(values[column.name], six.string_types)

    def test_row_get_values_join_meta_hashes(self, api_objects, data):
        """Test getting values for each row with meta, hashes, and a join str."""
        for row in data.rows:
            values = row.get_values(meta=True, hashes=True, join="\n")
            assert isinstance(values, dict)
            for column in data.columns:
                assert column.name in values
                assert isinstance(values[column.name], six.string_types)

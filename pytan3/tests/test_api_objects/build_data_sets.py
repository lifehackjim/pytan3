#!python
"""Generate data_sets.py using question data."""
import black
import os
import six
import sys
import time

if six.PY2:
    import pathlib2 as pathlib  # pragma: no cover
else:
    import pathlib


QUESTIONS = [
    {
        "text": (
            "Get Computer Name and IP Address and IP Route Details from all machines"
        ),
        "name": "data_name_ip_iproute",
    },
    {
        "text": ("Get Computer Name and IP Address from all machines"),
        "name": "data_name_ip",
    },
    {"text": ("Get Computer Name from all machines"), "name": "data_name"},
    # {
    #     "text": (
    #         "Get Computer Name and Installed Applications and Running Applications"
    #         " from all machines"
    #     ),
    #     "name": "data_name_iapp_rapp",
    # },
]

TMPL_FILE = '''# -*- coding: utf-8 -*-
"""Data sets for tests."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

{constructs}

data_sets = {data_sets}
'''

constructs = '''
constructs = {
    "soap": {
        "result_sets": {  # complex: ResultSetList
            "now": "2019/01/29 00:16:10 GMT-0000",  # simple
            "result_set": {  # complex: ResultSet
                "age": "0",  # simple
                "archived_question_id": "0",  # simple
                "cache_id": "2856562579",  # simple
                "error_count": "0",  # simple: # of errors in data set
                "estimated_total": "4",  # simple: # of clients
                "expiration": "0",  # simple
                "expire_seconds": "600",  # simple
                "filtered_row_count": "4",  # simple
                "filtered_row_count_machines": "4",  # simple
                "id": "29910",  # simple: question id that produced this data set
                "issue_seconds": "300",  # simple
                "item_count": "4",  # simple
                "mr_passed": "4",  # simple
                "mr_tested": "4",  # simple
                "no_results_count": "0",  # simple: # of no results in data set
                "passed": "4",  # simple: right side of the question is True
                "question_id": "29910",  # simple
                "report_count": "2",  # simple
                "row_count": "4",  # simple: # of rows in data set
                "row_count_machines": "4",  # simple
                "saved_question_id": "2234",  # simple
                "seconds_since_issued": "161",  # simple
                "select_count": "2",  # simple: # of sensors in question
                "tested": "4",  # simple: right side of the question evaluated
                "cs": {  # complex: ColumnList
                    "c": [  # ColumnList list attribute
                        # each column is indexed correlated to:
                        # each RowColumn in each RowColumnList in each Row
                        {  # complex: Column
                            "wh": "3409330187",  # simple: sensor hash owning column
                            "dn": "Computer Name",  # simple: display name of column
                            "rt": "1",  # simple: result type of column from sensor
                        },
                        {  # complex: Column
                            "wh": "3209138996",  # simple: sensor hash owning column
                            "dn": "IP Address",  # simple: display name of column
                            "rt": "5",  # simple: result type of column from sensor
                        },
                        {  # complex: Column
                            "wh": "0",  # simple: hash of sensor owning this column
                            "dn": "Count",  # simple: display name of sensor
                            "rt": "3",  # simple: result type of column from column
                        },
                    ]
                },
                "rs": {  # complex: RowList
                    "r": [  # RowList list attribute
                        {  # complex: Row
                            "id": "1214793340",  # simple
                            "cid": "3138344181",  # simple
                            "c": [  # complex: RowColumnList
                                {  # complex: RowColumn
                                    "v": {  # complex: RowValue (single value column)
                                        "h": "1655949567",  # simple: hash of value
                                        "text": "aquaman",  # simple: value of column
                                    }
                                },
                                {  # complex: RowColumn
                                    "v": [
                                        {  # complex: RowValue (multi value column)
                                            "h": "2953088310",  # simple: hash of value
                                            "text": "fe80::35cc:dea:229e:8569"
                                            # simple: value for this column
                                        },
                                        {  # complex: RowValue (multi value column)
                                            "h": "4091148251",  # simple: hash of value
                                            "text": "192.168.1.42"
                                            # simple: value for this column
                                        },
                                    ]
                                },
                                {  # complex: RowColumn
                                    "v": "1"  # complex: RowValue (Count column)
                                },
                            ],
                        }
                    ]
                },
            },
        },
        "rest": {  # complex: ResultSetList
            "max_available_age": "",
            "now": "2019/02/18 15:23:02 GMT-0000",
            "result_sets": [  # ResultSetList list attribute
                {
                    "age": 0,  # simple
                    "archived_question_id": 0,  # simple
                    "cache_id": "1333953524",  # simple
                    "error_count": 0,  # simple
                    "estimated_total": 4,  # simple
                    "expiration": 0,  # simple
                    "expire_seconds": 0,  # simple
                    "filtered_row_count": 4,  # simple
                    "filtered_row_count_machines": 4,  # simple
                    "id": 37299,  # simple
                    "issue_seconds": 0,  # simple
                    "item_count": 4,  # simple
                    "mr_passed": 4,  # simple
                    "mr_tested": 4,  # simple
                    "no_results_count": 0,  # simple
                    "passed": 4,  # simple
                    "question_id": 37299,  # simple
                    "report_count": 3,  # simple
                    "row_count": 4,  # simple
                    "row_count_machines": 4,  # simple
                    "saved_question_id": 0,  # simple
                    "seconds_since_issued": 0,  # simple
                    "select_count": 2,  # simple
                    "tested": 4,  # simple
                    "columns": [  # complex: ColumnList
                        {  # complex: Column
                            "hash": 3409330187,
                            "name": "Computer Name",
                            "type": 1,
                        },
                        {  # complex: Column
                            "hash": 3209138996,
                            "name": "IP Address",
                            "type": 5,
                        },
                        {"hash": 0, "name": "Count", "type": 3},  # complex: Column
                    ],
                    "rows": [  # complex: RowList
                        {  # complex: Row
                            "cid": 3138344181,
                            "data": [  # complex: RowColumnList
                                [  # complex: RowColumn
                                    {"hash": 1655949567, "text": "aquaman"}  # RowValue
                                ],
                                [  # complex: RowColumn
                                    {
                                        "hash": 2953088310,
                                        "text": "fe80::35cc:dea:229e:8569",
                                    },
                                    {"hash": 4091148251, "text": "192.168.1.42"},
                                ],
                                [{"text": "1"}],  # RowColumn {RowValue}
                            ],
                            "id": 1214793340,
                        }
                    ],
                }
            ],
        },
    }
}
"""Breakdown of how data sets map to API objects."""
'''

if __name__ == "__main__":
    THIS_DIR = pathlib.Path(sys.argv[0]).absolute().parent
    PKG_ROOT = THIS_DIR.parent.parent.parent
    sys.path.insert(0, format(PKG_ROOT))

    import pytan3  # noqa: E402

    promptness = pytan3.utils.prompts.promptness

    PYTAN_URL = os.environ.get("PYTAN_URL", None) or None
    PYTAN_API_TYPE = os.environ.get("PYTAN_API_TYPE", None) or None
    PYTAN_USERNAME = os.environ.get("PYTAN_USERNAME", None) or None
    PYTAN_PASSWORD = os.environ.get("PYTAN_PASSWORD", None) or None
    PYTAN_LEVEL = os.environ.get("PYTAN_LEVEL", None) or None

    url = PYTAN_URL or promptness.ask_str(
        text="Provide Tanium URL", default=None, env_var="PYTAN_URL"
    )
    username = PYTAN_USERNAME or promptness.ask_str(
        text="Provide Tanium Administrator Username",
        default="Administrator",
        env_var="PYTAN_USERNAME",
    )
    password = PYTAN_PASSWORD or promptness.ask_str(
        text="Provide Tanium Administrator Password",
        default=None,
        secure=True,
        env_var="PYTAN_PASSWORD",
    )
    lvl = PYTAN_LEVEL or promptness.ask_str(
        text="Provide Logging level", default="INFO", env_var="PYTAN_LEVEL"
    )

    path = THIS_DIR / "data"

    pytan3.utils.logs.add_stderr(lvl="DEBUG")
    client = pytan3.http_client.HttpClient(url=url, lvl=PYTAN_LEVEL)
    client.certify()

    auth = pytan3.auth_methods.Credentials(
        http_client=client, username=username, password=password, lvl=PYTAN_LEVEL
    )

    soap_adapter_cls = pytan3.adapters.load_type("soap")
    soap_api_client_cls = pytan3.api_clients.load_type("soap")
    soap_api_objects = pytan3.api_objects.load("soap")

    soap_api_client = soap_api_client_cls(http_client=client, auth_method=auth, lvl=lvl)
    soap_adapter = soap_adapter_cls(
        api_client=soap_api_client, api_objects=soap_api_objects, lvl=lvl
    )

    rest_adapter_cls = pytan3.adapters.load_type("rest")
    rest_api_client_cls = pytan3.api_clients.load_type("rest")
    rest_api_objects = pytan3.api_objects.load("rest")

    rest_api_client = rest_api_client_cls(http_client=client, auth_method=auth, lvl=lvl)
    rest_adapter = rest_adapter_cls(
        api_client=rest_api_client, api_objects=rest_api_objects, lvl=lvl
    )

    def parse_question(adapter, text):
        """P."""
        parse_result = adapter.api_parse_question(text)
        parses = parse_result()

        add_result = adapter.api_add_parsed_question(parses[0])
        added_question = add_result()

        question_result = adapter.api_get(added_question)
        question = question_result()
        m = ["Asked question: {q!r} using adapter:", "{adapter}"]
        m = "\n".join(m)
        m = m.format(q=question.query_text, adapter=adapter)
        pytan3.LOG.info(m)

        while True:
            time.sleep(1)
            info_result = adapter.api_get_result_info(question)
            info_sets = info_result()
            info_set = info_sets[0]
            m = ["Waiting for all answers for question {q!r}:", "{ri}"]
            m = "\n".join(m)
            m = m.format(q=question.query_text, ri=info_set)
            pytan3.LOG.info(m)
            if info_set.mr_tested >= info_set.estimated_total:
                break

        data_result = adapter.api_get_result_data(question)
        m = ["Received answers for question {q!r}:", "{rd}", ""]
        m = "\n".join(m)
        m = m.format(q=question.query_text, rd=data_result)
        pytan3.LOG.info(m)

        return data_result

    data_sets = {}
    data_sets["soap"] = {}
    data_sets["rest"] = {}

    for question in QUESTIONS:
        text = question["text"]
        name = question["name"]
        soap_result = parse_question(adapter=soap_adapter, text=text)
        rest_result = parse_question(adapter=rest_adapter, text=text)
        data_sets["soap"][name] = soap_result.data_obj["result_sets"]
        data_sets["rest"][name] = rest_result.data_obj

    contents = TMPL_FILE.format(data_sets=data_sets, constructs=constructs)
    contents = black.format_file_contents(
        src_contents=contents, line_length=88, fast=False
    )

    output_file = "data_sets.py"
    output_path = THIS_DIR / output_file
    output_path.write_text(contents)
    m = "Generated {path!r}"
    m = m.format(path=format(output_path))
    pytan3.LOG.info(m)

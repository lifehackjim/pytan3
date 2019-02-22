# -*- coding: utf-8 -*-
"""Data sets for tests."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


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


data_sets = {
    "soap": {
        "data_name_ip_iproute": {
            "now": "2019/02/19 20:50:43 GMT-0000",
            "result_set": {
                "age": "0",
                "id": "38626",
                "report_count": "2",
                "saved_question_id": "0",
                "question_id": "38626",
                "archived_question_id": "0",
                "seconds_since_issued": "0",
                "issue_seconds": "0",
                "expire_seconds": "0",
                "tested": "4",
                "passed": "4",
                "mr_tested": "4",
                "mr_passed": "4",
                "estimated_total": "4",
                "select_count": "3",
                "error_count": "0",
                "no_results_count": "0",
                "cs": {
                    "c": [
                        {"wh": "3409330187", "dn": "Computer Name", "rt": "1"},
                        {"wh": "3209138996", "dn": "IP Address", "rt": "5"},
                        {"wh": "435227963", "dn": "Destination", "rt": "5"},
                        {"wh": "435227963", "dn": "Gateway", "rt": "5"},
                        {"wh": "435227963", "dn": "Mask", "rt": "1"},
                        {"wh": "435227963", "dn": "Flags", "rt": "1"},
                        {"wh": "435227963", "dn": "Metric", "rt": "9"},
                        {"wh": "435227963", "dn": "Interface", "rt": "1"},
                        {"wh": "0", "dn": "Count", "rt": "3"},
                    ]
                },
                "cache_id": "58691653",
                "expiration": "0",
                "filtered_row_count": "4",
                "filtered_row_count_machines": "4",
                "row_count": "4",
                "row_count_machines": "4",
                "item_count": "4",
                "rs": {
                    "r": [
                        {
                            "id": "816601709",
                            "cid": "4000115789",
                            "c": [
                                {"v": {"h": "1163752210", "text": "batgirl"}},
                                {
                                    "v": [
                                        {
                                            "h": "802820713",
                                            "text": "fe80::18c5:f87e:4d4d:b4dd",
                                        },
                                        {"h": "1767863391", "text": "192.168.1.163"},
                                        {
                                            "h": "2309777956",
                                            "text": "fe80::10b3:fdf6:9c52:2414",
                                        },
                                        {"h": "1767663726", "text": "192.168.1.159"},
                                        {
                                            "h": "4290333278",
                                            "text": "fe80::2c18:a1ff:feb4:a65a",
                                        },
                                        {
                                            "h": "3653249195",
                                            "text": "fe80::3a54:2d8f:b10a:d5ef",
                                        },
                                        {
                                            "h": "921109540",
                                            "text": "fe80::f8bd:82aa:b439:a5b",
                                        },
                                        {
                                            "h": "4175852127",
                                            "text": "fe80::3a19:b9cd:67e3:9696",
                                        },
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "240307004", "text": "default"},
                                        {"h": "2635419588", "text": "default"},
                                        {"h": "1293520294", "text": "169.254"},
                                        {"h": "1243717211", "text": "169.254"},
                                        {"h": "2429349248", "text": "169.254.130.68"},
                                        {"h": "1254249661", "text": "192.168.1"},
                                        {"h": "3620174818", "text": "192.168.1"},
                                        {"h": "2790691842", "text": "192.168.1.1/32"},
                                        {"h": "3152938599", "text": "192.168.1.1/32"},
                                        {"h": "3180038305", "text": "192.168.1.157"},
                                        {"h": "1548911636", "text": "192.168.1.159/32"},
                                        {"h": "2456110221", "text": "192.168.1.163/32"},
                                        {"h": "2804922501", "text": "224.0.0/4"},
                                        {"h": "4109726944", "text": "224.0.0/4"},
                                        {
                                            "h": "1154132299",
                                            "text": "255.255.255.255/32",
                                        },
                                        {
                                            "h": "2251533780",
                                            "text": "255.255.255.255/32",
                                        },
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "240307004", "text": "192.168.1.1"},
                                        {"h": "2635419588", "text": "192.168.1.1"},
                                        {"h": "1293520294", "text": "link#5"},
                                        {"h": "1243717211", "text": "link#8"},
                                        {"h": "2429349248", "text": "link#8"},
                                        {"h": "1254249661", "text": "link#5"},
                                        {"h": "3620174818", "text": "link#8"},
                                        {"h": "2790691842", "text": "link#5"},
                                        {"h": "3152938599", "text": "link#8"},
                                        {"h": "3180038305", "text": "link#8"},
                                        {"h": "1548911636", "text": "link#8"},
                                        {"h": "2456110221", "text": "link#5"},
                                        {"h": "2804922501", "text": "link#5"},
                                        {"h": "4109726944", "text": "link#8"},
                                        {"h": "1154132299", "text": "link#5"},
                                        {"h": "2251533780", "text": "link#8"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "240307004"},
                                        {"h": "2635419588"},
                                        {"h": "1293520294"},
                                        {"h": "1243717211"},
                                        {"h": "2429349248"},
                                        {"h": "1254249661"},
                                        {"h": "3620174818"},
                                        {"h": "2790691842"},
                                        {"h": "3152938599"},
                                        {"h": "3180038305"},
                                        {"h": "1548911636"},
                                        {"h": "2456110221"},
                                        {"h": "2804922501"},
                                        {"h": "4109726944"},
                                        {"h": "1154132299"},
                                        {"h": "2251533780"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "240307004", "text": "UGSc"},
                                        {"h": "2635419588", "text": "UGScI"},
                                        {"h": "1293520294", "text": "UCS"},
                                        {"h": "1243717211", "text": "UCSI"},
                                        {"h": "2429349248", "text": "UHLSW"},
                                        {"h": "1254249661", "text": "UCS"},
                                        {"h": "3620174818", "text": "UCSI"},
                                        {"h": "2790691842", "text": "UCS"},
                                        {"h": "3152938599", "text": "UCSI"},
                                        {"h": "3180038305", "text": "UHLWIi"},
                                        {"h": "1548911636", "text": "UCS"},
                                        {"h": "2456110221", "text": "UCS"},
                                        {"h": "2804922501", "text": "UmCS"},
                                        {"h": "4109726944", "text": "UmCSI"},
                                        {"h": "1154132299", "text": "UCS"},
                                        {"h": "2251533780", "text": "UCSI"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "240307004"},
                                        {"h": "2635419588"},
                                        {"h": "1293520294"},
                                        {"h": "1243717211"},
                                        {"h": "2429349248"},
                                        {"h": "1254249661"},
                                        {"h": "3620174818"},
                                        {"h": "2790691842"},
                                        {"h": "3152938599"},
                                        {"h": "3180038305"},
                                        {"h": "1548911636"},
                                        {"h": "2456110221"},
                                        {"h": "2804922501"},
                                        {"h": "4109726944"},
                                        {"h": "1154132299"},
                                        {"h": "2251533780"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "240307004", "text": "en0"},
                                        {"h": "2635419588", "text": "en1"},
                                        {"h": "1293520294", "text": "en0"},
                                        {"h": "1243717211", "text": "en1"},
                                        {"h": "2429349248", "text": "en1"},
                                        {"h": "1254249661", "text": "en0"},
                                        {"h": "3620174818", "text": "en1"},
                                        {"h": "2790691842", "text": "en0"},
                                        {"h": "3152938599", "text": "en1"},
                                        {"h": "3180038305", "text": "en1"},
                                        {"h": "1548911636", "text": "en1"},
                                        {"h": "2456110221", "text": "en0"},
                                        {"h": "2804922501", "text": "en0"},
                                        {"h": "4109726944", "text": "en1"},
                                        {"h": "1154132299", "text": "en0"},
                                        {"h": "2251533780", "text": "en1"},
                                    ]
                                },
                                {"v": "1"},
                            ],
                        },
                        {
                            "id": "336549400",
                            "cid": "3138344181",
                            "c": [
                                {"v": {"h": "1655949567", "text": "aquaman"}},
                                {
                                    "v": [
                                        {
                                            "h": "2953088310",
                                            "text": "fe80::35cc:dea:229e:8569",
                                        },
                                        {"h": "4091148251", "text": "192.168.1.42"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "577210383", "text": "0.0.0.0"},
                                        {"h": "1794293358", "text": "127.0.0.0"},
                                        {"h": "1174357489", "text": "127.0.0.1"},
                                        {"h": "2741067856", "text": "192.168.1.0"},
                                        {"h": "1858378260", "text": "192.168.1.42"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "577210383", "text": "192.168.1.1"},
                                        {"h": "1794293358", "text": "0.0.0.0"},
                                        {"h": "1174357489", "text": "0.0.0.0"},
                                        {"h": "2741067856", "text": "0.0.0.0"},
                                        {"h": "1858378260", "text": "0.0.0.0"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "577210383", "text": "0.0.0.0"},
                                        {"h": "1794293358", "text": "255.0.0.0"},
                                        {"h": "1174357489", "text": "255.255.255.255"},
                                        {"h": "2741067856", "text": "255.255.255.0"},
                                        {"h": "1858378260", "text": "255.255.255.255"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "577210383", "text": "-"},
                                        {"h": "1794293358", "text": "-"},
                                        {"h": "1174357489", "text": "-"},
                                        {"h": "2741067856", "text": "-"},
                                        {"h": "1858378260", "text": "-"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "577210383", "text": "261"},
                                        {"h": "1794293358", "text": "306"},
                                        {"h": "1174357489", "text": "306"},
                                        {"h": "2741067856", "text": "261"},
                                        {"h": "1858378260", "text": "261"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "577210383", "text": "-"},
                                        {"h": "1794293358", "text": "-"},
                                        {"h": "1174357489", "text": "-"},
                                        {"h": "2741067856", "text": "-"},
                                        {"h": "1858378260", "text": "-"},
                                    ]
                                },
                                {"v": "1"},
                            ],
                        },
                        {
                            "id": "3557650850",
                            "cid": "105187931",
                            "c": [
                                {"v": {"h": "2779630309", "text": "cyborg"}},
                                {
                                    "v": [
                                        {
                                            "h": "1051494381",
                                            "text": "fe80::f8ae:36e5:2526:c0",
                                        },
                                        {"h": "4092094376", "text": "192.168.1.32"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "577210383", "text": "0.0.0.0"},
                                        {"h": "1794293358", "text": "127.0.0.0"},
                                        {"h": "1174357489", "text": "127.0.0.1"},
                                        {"h": "2741067856", "text": "192.168.1.0"},
                                        {"h": "537302195", "text": "192.168.1.32"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "577210383", "text": "192.168.1.1"},
                                        {"h": "1794293358", "text": "0.0.0.0"},
                                        {"h": "1174357489", "text": "0.0.0.0"},
                                        {"h": "2741067856", "text": "0.0.0.0"},
                                        {"h": "537302195", "text": "0.0.0.0"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "577210383", "text": "0.0.0.0"},
                                        {"h": "1794293358", "text": "255.0.0.0"},
                                        {"h": "1174357489", "text": "255.255.255.255"},
                                        {"h": "2741067856", "text": "255.255.255.0"},
                                        {"h": "537302195", "text": "255.255.255.255"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "577210383", "text": "-"},
                                        {"h": "1794293358", "text": "-"},
                                        {"h": "1174357489", "text": "-"},
                                        {"h": "2741067856", "text": "-"},
                                        {"h": "537302195", "text": "-"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "577210383", "text": "261"},
                                        {"h": "1794293358", "text": "306"},
                                        {"h": "1174357489", "text": "306"},
                                        {"h": "2741067856", "text": "261"},
                                        {"h": "537302195", "text": "261"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "577210383", "text": "-"},
                                        {"h": "1794293358", "text": "-"},
                                        {"h": "1174357489", "text": "-"},
                                        {"h": "2741067856", "text": "-"},
                                        {"h": "537302195", "text": "-"},
                                    ]
                                },
                                {"v": "1"},
                            ],
                        },
                        {
                            "id": "3165480407",
                            "cid": "1777856850",
                            "c": [
                                {"v": {"h": "3744311725", "text": "metallo"}},
                                {
                                    "v": [
                                        {"h": "4091148686", "text": "192.168.1.41"},
                                        {
                                            "h": "3155276204",
                                            "text": "fe80::b46b:3af2:f7ec:e879",
                                        },
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "4129021854", "text": "0.0.0.0"},
                                        {"h": "1181525525", "text": "169.254.0.0"},
                                        {"h": "1030919274", "text": "192.168.1.0"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "4129021854", "text": "192.168.1.1"},
                                        {"h": "1181525525", "text": "0.0.0.0"},
                                        {"h": "1030919274", "text": "0.0.0.0"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "4129021854", "text": "0.0.0.0"},
                                        {"h": "1181525525", "text": "255.255.0.0"},
                                        {"h": "1030919274", "text": "255.255.255.0"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "4129021854", "text": "UG"},
                                        {"h": "1181525525", "text": "U"},
                                        {"h": "1030919274", "text": "U"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "4129021854", "text": "100"},
                                        {"h": "1181525525", "text": "1000"},
                                        {"h": "1030919274", "text": "100"},
                                    ]
                                },
                                {
                                    "v": [
                                        {"h": "4129021854", "text": "ens18"},
                                        {"h": "1181525525", "text": "ens18"},
                                        {"h": "1030919274", "text": "ens18"},
                                    ]
                                },
                                {"v": "1"},
                            ],
                        },
                    ]
                },
            },
        },
        "data_name_ip": {
            "now": "2019/02/19 20:50:49 GMT-0000",
            "result_set": {
                "age": "0",
                "id": "38628",
                "report_count": "2",
                "saved_question_id": "0",
                "question_id": "38628",
                "archived_question_id": "0",
                "seconds_since_issued": "0",
                "issue_seconds": "0",
                "expire_seconds": "0",
                "tested": "4",
                "passed": "4",
                "mr_tested": "4",
                "mr_passed": "4",
                "estimated_total": "4",
                "select_count": "2",
                "error_count": "0",
                "no_results_count": "0",
                "cs": {
                    "c": [
                        {"wh": "3409330187", "dn": "Computer Name", "rt": "1"},
                        {"wh": "3209138996", "dn": "IP Address", "rt": "5"},
                        {"wh": "0", "dn": "Count", "rt": "3"},
                    ]
                },
                "cache_id": "561443203",
                "expiration": "0",
                "filtered_row_count": "4",
                "filtered_row_count_machines": "4",
                "row_count": "4",
                "row_count_machines": "4",
                "item_count": "4",
                "rs": {
                    "r": [
                        {
                            "id": "1012823231",
                            "cid": "4000115789",
                            "c": [
                                {"v": {"h": "1163752210", "text": "batgirl"}},
                                {
                                    "v": [
                                        {
                                            "h": "802820713",
                                            "text": "fe80::18c5:f87e:4d4d:b4dd",
                                        },
                                        {"h": "1767863391", "text": "192.168.1.163"},
                                        {
                                            "h": "2309777956",
                                            "text": "fe80::10b3:fdf6:9c52:2414",
                                        },
                                        {"h": "1767663726", "text": "192.168.1.159"},
                                        {
                                            "h": "4290333278",
                                            "text": "fe80::2c18:a1ff:feb4:a65a",
                                        },
                                        {
                                            "h": "3653249195",
                                            "text": "fe80::3a54:2d8f:b10a:d5ef",
                                        },
                                        {
                                            "h": "921109540",
                                            "text": "fe80::f8bd:82aa:b439:a5b",
                                        },
                                        {
                                            "h": "4175852127",
                                            "text": "fe80::3a19:b9cd:67e3:9696",
                                        },
                                    ]
                                },
                                {"v": "1"},
                            ],
                        },
                        {
                            "id": "1214793340",
                            "cid": "3138344181",
                            "c": [
                                {"v": {"h": "1655949567", "text": "aquaman"}},
                                {
                                    "v": [
                                        {
                                            "h": "2953088310",
                                            "text": "fe80::35cc:dea:229e:8569",
                                        },
                                        {"h": "4091148251", "text": "192.168.1.42"},
                                    ]
                                },
                                {"v": "1"},
                            ],
                        },
                        {
                            "id": "1160483416",
                            "cid": "105187931",
                            "c": [
                                {"v": {"h": "2779630309", "text": "cyborg"}},
                                {
                                    "v": [
                                        {
                                            "h": "1051494381",
                                            "text": "fe80::f8ae:36e5:2526:c0",
                                        },
                                        {"h": "4092094376", "text": "192.168.1.32"},
                                    ]
                                },
                                {"v": "1"},
                            ],
                        },
                        {
                            "id": "4291310295",
                            "cid": "1777856850",
                            "c": [
                                {"v": {"h": "3744311725", "text": "metallo"}},
                                {
                                    "v": [
                                        {"h": "4091148686", "text": "192.168.1.41"},
                                        {
                                            "h": "3155276204",
                                            "text": "fe80::b46b:3af2:f7ec:e879",
                                        },
                                    ]
                                },
                                {"v": "1"},
                            ],
                        },
                    ]
                },
            },
        },
        "data_name": {
            "now": "2019/02/19 20:51:01 GMT-0000",
            "result_set": {
                "age": "0",
                "id": "38630",
                "report_count": "2",
                "saved_question_id": "0",
                "question_id": "38630",
                "archived_question_id": "0",
                "seconds_since_issued": "0",
                "issue_seconds": "0",
                "expire_seconds": "0",
                "tested": "4",
                "passed": "4",
                "mr_tested": "4",
                "mr_passed": "4",
                "estimated_total": "4",
                "select_count": "1",
                "error_count": "0",
                "no_results_count": "0",
                "cs": {
                    "c": [
                        {"wh": "3409330187", "dn": "Computer Name", "rt": "1"},
                        {"wh": "0", "dn": "Count", "rt": "3"},
                    ]
                },
                "cache_id": "1950349412",
                "expiration": "0",
                "filtered_row_count": "4",
                "filtered_row_count_machines": "4",
                "row_count": "4",
                "row_count_machines": "4",
                "item_count": "4",
                "rs": {
                    "r": [
                        {
                            "id": "2077176149",
                            "cid": "4000115789",
                            "c": [
                                {"v": {"h": "1163752210", "text": "batgirl"}},
                                {"v": "1"},
                            ],
                        },
                        {
                            "id": "2454882914",
                            "cid": "3138344181",
                            "c": [
                                {"v": {"h": "1655949567", "text": "aquaman"}},
                                {"v": "1"},
                            ],
                        },
                        {
                            "id": "3682778715",
                            "cid": "105187931",
                            "c": [
                                {"v": {"h": "2779630309", "text": "cyborg"}},
                                {"v": "1"},
                            ],
                        },
                        {
                            "id": "2734563840",
                            "cid": "1777856850",
                            "c": [
                                {"v": {"h": "3744311725", "text": "metallo"}},
                                {"v": "1"},
                            ],
                        },
                    ]
                },
            },
        },
    },
    "rest": {
        "data_name_ip_iproute": {
            "max_available_age": "",
            "now": "2019/02/19 20:50:44 GMT-0000",
            "result_sets": [
                {
                    "age": 0,
                    "archived_question_id": 0,
                    "cache_id": "1643634172",
                    "columns": [
                        {"hash": 3409330187, "name": "Computer Name", "type": 1},
                        {"hash": 3209138996, "name": "IP Address", "type": 5},
                        {"hash": 435227963, "name": "Destination", "type": 5},
                        {"hash": 435227963, "name": "Gateway", "type": 5},
                        {"hash": 435227963, "name": "Mask", "type": 1},
                        {"hash": 435227963, "name": "Flags", "type": 1},
                        {"hash": 435227963, "name": "Metric", "type": 9},
                        {"hash": 435227963, "name": "Interface", "type": 1},
                        {"hash": 0, "name": "Count", "type": 3},
                    ],
                    "error_count": 0,
                    "estimated_total": 4,
                    "expiration": 0,
                    "expire_seconds": 0,
                    "filtered_row_count": 4,
                    "filtered_row_count_machines": 4,
                    "id": 38627,
                    "issue_seconds": 0,
                    "item_count": 4,
                    "mr_passed": 4,
                    "mr_tested": 4,
                    "no_results_count": 0,
                    "passed": 4,
                    "question_id": 38627,
                    "report_count": 1,
                    "row_count": 4,
                    "row_count_machines": 4,
                    "rows": [
                        {
                            "cid": 4000115789,
                            "data": [
                                [{"hash": 1163752210, "text": "batgirl"}],
                                [
                                    {
                                        "hash": 802820713,
                                        "text": "fe80::18c5:f87e:4d4d:b4dd",
                                    },
                                    {"hash": 1767863391, "text": "192.168.1.163"},
                                    {
                                        "hash": 2309777956,
                                        "text": "fe80::10b3:fdf6:9c52:2414",
                                    },
                                    {"hash": 1767663726, "text": "192.168.1.159"},
                                    {
                                        "hash": 4290333278,
                                        "text": "fe80::2c18:a1ff:feb4:a65a",
                                    },
                                    {
                                        "hash": 3653249195,
                                        "text": "fe80::3a54:2d8f:b10a:d5ef",
                                    },
                                    {
                                        "hash": 921109540,
                                        "text": "fe80::f8bd:82aa:b439:a5b",
                                    },
                                    {
                                        "hash": 4175852127,
                                        "text": "fe80::3a19:b9cd:67e3:9696",
                                    },
                                ],
                                [
                                    {"hash": 240307004, "text": "default"},
                                    {"hash": 2635419588, "text": "default"},
                                    {"hash": 1293520294, "text": "169.254"},
                                    {"hash": 1243717211, "text": "169.254"},
                                    {"hash": 2429349248, "text": "169.254.130.68"},
                                    {"hash": 1254249661, "text": "192.168.1"},
                                    {"hash": 3620174818, "text": "192.168.1"},
                                    {"hash": 2790691842, "text": "192.168.1.1/32"},
                                    {"hash": 3152938599, "text": "192.168.1.1/32"},
                                    {"hash": 3180038305, "text": "192.168.1.157"},
                                    {"hash": 1548911636, "text": "192.168.1.159/32"},
                                    {"hash": 2456110221, "text": "192.168.1.163/32"},
                                    {"hash": 2804922501, "text": "224.0.0/4"},
                                    {"hash": 4109726944, "text": "224.0.0/4"},
                                    {"hash": 1154132299, "text": "255.255.255.255/32"},
                                    {"hash": 2251533780, "text": "255.255.255.255/32"},
                                ],
                                [
                                    {"hash": 240307004, "text": "192.168.1.1"},
                                    {"hash": 2635419588, "text": "192.168.1.1"},
                                    {"hash": 1293520294, "text": "link#5"},
                                    {"hash": 1243717211, "text": "link#8"},
                                    {"hash": 2429349248, "text": "link#8"},
                                    {"hash": 1254249661, "text": "link#5"},
                                    {"hash": 3620174818, "text": "link#8"},
                                    {"hash": 2790691842, "text": "link#5"},
                                    {"hash": 3152938599, "text": "link#8"},
                                    {"hash": 3180038305, "text": "link#8"},
                                    {"hash": 1548911636, "text": "link#8"},
                                    {"hash": 2456110221, "text": "link#5"},
                                    {"hash": 2804922501, "text": "link#5"},
                                    {"hash": 4109726944, "text": "link#8"},
                                    {"hash": 1154132299, "text": "link#5"},
                                    {"hash": 2251533780, "text": "link#8"},
                                ],
                                [
                                    {"hash": 240307004, "text": ""},
                                    {"hash": 2635419588, "text": ""},
                                    {"hash": 1293520294, "text": ""},
                                    {"hash": 1243717211, "text": ""},
                                    {"hash": 2429349248, "text": ""},
                                    {"hash": 1254249661, "text": ""},
                                    {"hash": 3620174818, "text": ""},
                                    {"hash": 2790691842, "text": ""},
                                    {"hash": 3152938599, "text": ""},
                                    {"hash": 3180038305, "text": ""},
                                    {"hash": 1548911636, "text": ""},
                                    {"hash": 2456110221, "text": ""},
                                    {"hash": 2804922501, "text": ""},
                                    {"hash": 4109726944, "text": ""},
                                    {"hash": 1154132299, "text": ""},
                                    {"hash": 2251533780, "text": ""},
                                ],
                                [
                                    {"hash": 240307004, "text": "UGSc"},
                                    {"hash": 2635419588, "text": "UGScI"},
                                    {"hash": 1293520294, "text": "UCS"},
                                    {"hash": 1243717211, "text": "UCSI"},
                                    {"hash": 2429349248, "text": "UHLSW"},
                                    {"hash": 1254249661, "text": "UCS"},
                                    {"hash": 3620174818, "text": "UCSI"},
                                    {"hash": 2790691842, "text": "UCS"},
                                    {"hash": 3152938599, "text": "UCSI"},
                                    {"hash": 3180038305, "text": "UHLWIi"},
                                    {"hash": 1548911636, "text": "UCS"},
                                    {"hash": 2456110221, "text": "UCS"},
                                    {"hash": 2804922501, "text": "UmCS"},
                                    {"hash": 4109726944, "text": "UmCSI"},
                                    {"hash": 1154132299, "text": "UCS"},
                                    {"hash": 2251533780, "text": "UCSI"},
                                ],
                                [
                                    {"hash": 240307004, "text": ""},
                                    {"hash": 2635419588, "text": ""},
                                    {"hash": 1293520294, "text": ""},
                                    {"hash": 1243717211, "text": ""},
                                    {"hash": 2429349248, "text": ""},
                                    {"hash": 1254249661, "text": ""},
                                    {"hash": 3620174818, "text": ""},
                                    {"hash": 2790691842, "text": ""},
                                    {"hash": 3152938599, "text": ""},
                                    {"hash": 3180038305, "text": ""},
                                    {"hash": 1548911636, "text": ""},
                                    {"hash": 2456110221, "text": ""},
                                    {"hash": 2804922501, "text": ""},
                                    {"hash": 4109726944, "text": ""},
                                    {"hash": 1154132299, "text": ""},
                                    {"hash": 2251533780, "text": ""},
                                ],
                                [
                                    {"hash": 240307004, "text": "en0"},
                                    {"hash": 2635419588, "text": "en1"},
                                    {"hash": 1293520294, "text": "en0"},
                                    {"hash": 1243717211, "text": "en1"},
                                    {"hash": 2429349248, "text": "en1"},
                                    {"hash": 1254249661, "text": "en0"},
                                    {"hash": 3620174818, "text": "en1"},
                                    {"hash": 2790691842, "text": "en0"},
                                    {"hash": 3152938599, "text": "en1"},
                                    {"hash": 3180038305, "text": "en1"},
                                    {"hash": 1548911636, "text": "en1"},
                                    {"hash": 2456110221, "text": "en0"},
                                    {"hash": 2804922501, "text": "en0"},
                                    {"hash": 4109726944, "text": "en1"},
                                    {"hash": 1154132299, "text": "en0"},
                                    {"hash": 2251533780, "text": "en1"},
                                ],
                                [{"text": "1"}],
                            ],
                            "id": 816601709,
                        },
                        {
                            "cid": 3138344181,
                            "data": [
                                [{"hash": 1655949567, "text": "aquaman"}],
                                [
                                    {
                                        "hash": 2953088310,
                                        "text": "fe80::35cc:dea:229e:8569",
                                    },
                                    {"hash": 4091148251, "text": "192.168.1.42"},
                                ],
                                [
                                    {"hash": 577210383, "text": "0.0.0.0"},
                                    {"hash": 1794293358, "text": "127.0.0.0"},
                                    {"hash": 1174357489, "text": "127.0.0.1"},
                                    {"hash": 2741067856, "text": "192.168.1.0"},
                                    {"hash": 1858378260, "text": "192.168.1.42"},
                                ],
                                [
                                    {"hash": 577210383, "text": "192.168.1.1"},
                                    {"hash": 1794293358, "text": "0.0.0.0"},
                                    {"hash": 1174357489, "text": "0.0.0.0"},
                                    {"hash": 2741067856, "text": "0.0.0.0"},
                                    {"hash": 1858378260, "text": "0.0.0.0"},
                                ],
                                [
                                    {"hash": 577210383, "text": "0.0.0.0"},
                                    {"hash": 1794293358, "text": "255.0.0.0"},
                                    {"hash": 1174357489, "text": "255.255.255.255"},
                                    {"hash": 2741067856, "text": "255.255.255.0"},
                                    {"hash": 1858378260, "text": "255.255.255.255"},
                                ],
                                [
                                    {"hash": 577210383, "text": "-"},
                                    {"hash": 1794293358, "text": "-"},
                                    {"hash": 1174357489, "text": "-"},
                                    {"hash": 2741067856, "text": "-"},
                                    {"hash": 1858378260, "text": "-"},
                                ],
                                [
                                    {"hash": 577210383, "text": "261"},
                                    {"hash": 1794293358, "text": "306"},
                                    {"hash": 1174357489, "text": "306"},
                                    {"hash": 2741067856, "text": "261"},
                                    {"hash": 1858378260, "text": "261"},
                                ],
                                [
                                    {"hash": 577210383, "text": "-"},
                                    {"hash": 1794293358, "text": "-"},
                                    {"hash": 1174357489, "text": "-"},
                                    {"hash": 2741067856, "text": "-"},
                                    {"hash": 1858378260, "text": "-"},
                                ],
                                [{"text": "1"}],
                            ],
                            "id": 336549400,
                        },
                        {
                            "cid": 105187931,
                            "data": [
                                [{"hash": 2779630309, "text": "cyborg"}],
                                [
                                    {
                                        "hash": 1051494381,
                                        "text": "fe80::f8ae:36e5:2526:c0",
                                    },
                                    {"hash": 4092094376, "text": "192.168.1.32"},
                                ],
                                [
                                    {"hash": 577210383, "text": "0.0.0.0"},
                                    {"hash": 1794293358, "text": "127.0.0.0"},
                                    {"hash": 1174357489, "text": "127.0.0.1"},
                                    {"hash": 2741067856, "text": "192.168.1.0"},
                                    {"hash": 537302195, "text": "192.168.1.32"},
                                ],
                                [
                                    {"hash": 577210383, "text": "192.168.1.1"},
                                    {"hash": 1794293358, "text": "0.0.0.0"},
                                    {"hash": 1174357489, "text": "0.0.0.0"},
                                    {"hash": 2741067856, "text": "0.0.0.0"},
                                    {"hash": 537302195, "text": "0.0.0.0"},
                                ],
                                [
                                    {"hash": 577210383, "text": "0.0.0.0"},
                                    {"hash": 1794293358, "text": "255.0.0.0"},
                                    {"hash": 1174357489, "text": "255.255.255.255"},
                                    {"hash": 2741067856, "text": "255.255.255.0"},
                                    {"hash": 537302195, "text": "255.255.255.255"},
                                ],
                                [
                                    {"hash": 577210383, "text": "-"},
                                    {"hash": 1794293358, "text": "-"},
                                    {"hash": 1174357489, "text": "-"},
                                    {"hash": 2741067856, "text": "-"},
                                    {"hash": 537302195, "text": "-"},
                                ],
                                [
                                    {"hash": 577210383, "text": "261"},
                                    {"hash": 1794293358, "text": "306"},
                                    {"hash": 1174357489, "text": "306"},
                                    {"hash": 2741067856, "text": "261"},
                                    {"hash": 537302195, "text": "261"},
                                ],
                                [
                                    {"hash": 577210383, "text": "-"},
                                    {"hash": 1794293358, "text": "-"},
                                    {"hash": 1174357489, "text": "-"},
                                    {"hash": 2741067856, "text": "-"},
                                    {"hash": 537302195, "text": "-"},
                                ],
                                [{"text": "1"}],
                            ],
                            "id": 3557650850,
                        },
                        {
                            "cid": 1777856850,
                            "data": [
                                [{"hash": 3744311725, "text": "metallo"}],
                                [
                                    {"hash": 4091148686, "text": "192.168.1.41"},
                                    {
                                        "hash": 3155276204,
                                        "text": "fe80::b46b:3af2:f7ec:e879",
                                    },
                                ],
                                [
                                    {"hash": 4129021854, "text": "0.0.0.0"},
                                    {"hash": 1181525525, "text": "169.254.0.0"},
                                    {"hash": 1030919274, "text": "192.168.1.0"},
                                ],
                                [
                                    {"hash": 4129021854, "text": "192.168.1.1"},
                                    {"hash": 1181525525, "text": "0.0.0.0"},
                                    {"hash": 1030919274, "text": "0.0.0.0"},
                                ],
                                [
                                    {"hash": 4129021854, "text": "0.0.0.0"},
                                    {"hash": 1181525525, "text": "255.255.0.0"},
                                    {"hash": 1030919274, "text": "255.255.255.0"},
                                ],
                                [
                                    {"hash": 4129021854, "text": "UG"},
                                    {"hash": 1181525525, "text": "U"},
                                    {"hash": 1030919274, "text": "U"},
                                ],
                                [
                                    {"hash": 4129021854, "text": "100"},
                                    {"hash": 1181525525, "text": "1000"},
                                    {"hash": 1030919274, "text": "100"},
                                ],
                                [
                                    {"hash": 4129021854, "text": "ens18"},
                                    {"hash": 1181525525, "text": "ens18"},
                                    {"hash": 1030919274, "text": "ens18"},
                                ],
                                [{"text": "1"}],
                            ],
                            "id": 3165480407,
                        },
                    ],
                    "saved_question_id": 0,
                    "seconds_since_issued": 0,
                    "select_count": 3,
                    "tested": 4,
                }
            ],
        },
        "data_name_ip": {
            "max_available_age": "",
            "now": "2019/02/19 20:50:55 GMT-0000",
            "result_sets": [
                {
                    "age": 0,
                    "archived_question_id": 0,
                    "cache_id": "3629138501",
                    "columns": [
                        {"hash": 3409330187, "name": "Computer Name", "type": 1},
                        {"hash": 3209138996, "name": "IP Address", "type": 5},
                        {"hash": 0, "name": "Count", "type": 3},
                    ],
                    "error_count": 0,
                    "estimated_total": 4,
                    "expiration": 0,
                    "expire_seconds": 0,
                    "filtered_row_count": 4,
                    "filtered_row_count_machines": 4,
                    "id": 38629,
                    "issue_seconds": 0,
                    "item_count": 4,
                    "mr_passed": 4,
                    "mr_tested": 4,
                    "no_results_count": 0,
                    "passed": 4,
                    "question_id": 38629,
                    "report_count": 2,
                    "row_count": 4,
                    "row_count_machines": 4,
                    "rows": [
                        {
                            "cid": 4000115789,
                            "data": [
                                [{"hash": 1163752210, "text": "batgirl"}],
                                [
                                    {
                                        "hash": 802820713,
                                        "text": "fe80::18c5:f87e:4d4d:b4dd",
                                    },
                                    {"hash": 1767863391, "text": "192.168.1.163"},
                                    {
                                        "hash": 2309777956,
                                        "text": "fe80::10b3:fdf6:9c52:2414",
                                    },
                                    {"hash": 1767663726, "text": "192.168.1.159"},
                                    {
                                        "hash": 4290333278,
                                        "text": "fe80::2c18:a1ff:feb4:a65a",
                                    },
                                    {
                                        "hash": 3653249195,
                                        "text": "fe80::3a54:2d8f:b10a:d5ef",
                                    },
                                    {
                                        "hash": 921109540,
                                        "text": "fe80::f8bd:82aa:b439:a5b",
                                    },
                                    {
                                        "hash": 4175852127,
                                        "text": "fe80::3a19:b9cd:67e3:9696",
                                    },
                                ],
                                [{"text": "1"}],
                            ],
                            "id": 1012823231,
                        },
                        {
                            "cid": 3138344181,
                            "data": [
                                [{"hash": 1655949567, "text": "aquaman"}],
                                [
                                    {
                                        "hash": 2953088310,
                                        "text": "fe80::35cc:dea:229e:8569",
                                    },
                                    {"hash": 4091148251, "text": "192.168.1.42"},
                                ],
                                [{"text": "1"}],
                            ],
                            "id": 1214793340,
                        },
                        {
                            "cid": 105187931,
                            "data": [
                                [{"hash": 2779630309, "text": "cyborg"}],
                                [
                                    {
                                        "hash": 1051494381,
                                        "text": "fe80::f8ae:36e5:2526:c0",
                                    },
                                    {"hash": 4092094376, "text": "192.168.1.32"},
                                ],
                                [{"text": "1"}],
                            ],
                            "id": 1160483416,
                        },
                        {
                            "cid": 1777856850,
                            "data": [
                                [{"hash": 3744311725, "text": "metallo"}],
                                [
                                    {"hash": 4091148686, "text": "192.168.1.41"},
                                    {
                                        "hash": 3155276204,
                                        "text": "fe80::b46b:3af2:f7ec:e879",
                                    },
                                ],
                                [{"text": "1"}],
                            ],
                            "id": 4291310295,
                        },
                    ],
                    "saved_question_id": 0,
                    "seconds_since_issued": 0,
                    "select_count": 2,
                    "tested": 4,
                }
            ],
        },
        "data_name": {
            "max_available_age": "",
            "now": "2019/02/19 20:51:07 GMT-0000",
            "result_sets": [
                {
                    "age": 0,
                    "archived_question_id": 0,
                    "cache_id": "2452210938",
                    "columns": [
                        {"hash": 3409330187, "name": "Computer Name", "type": 1},
                        {"hash": 0, "name": "Count", "type": 3},
                    ],
                    "error_count": 0,
                    "estimated_total": 4,
                    "expiration": 0,
                    "expire_seconds": 0,
                    "filtered_row_count": 4,
                    "filtered_row_count_machines": 4,
                    "id": 38631,
                    "issue_seconds": 0,
                    "item_count": 4,
                    "mr_passed": 4,
                    "mr_tested": 4,
                    "no_results_count": 0,
                    "passed": 4,
                    "question_id": 38631,
                    "report_count": 2,
                    "row_count": 4,
                    "row_count_machines": 4,
                    "rows": [
                        {
                            "cid": 4000115789,
                            "data": [
                                [{"hash": 1163752210, "text": "batgirl"}],
                                [{"text": "1"}],
                            ],
                            "id": 2077176149,
                        },
                        {
                            "cid": 3138344181,
                            "data": [
                                [{"hash": 1655949567, "text": "aquaman"}],
                                [{"text": "1"}],
                            ],
                            "id": 2454882914,
                        },
                        {
                            "cid": 105187931,
                            "data": [
                                [{"hash": 2779630309, "text": "cyborg"}],
                                [{"text": "1"}],
                            ],
                            "id": 3682778715,
                        },
                        {
                            "cid": 1777856850,
                            "data": [
                                [{"hash": 3744311725, "text": "metallo"}],
                                [{"text": "1"}],
                            ],
                            "id": 2734563840,
                        },
                    ],
                    "saved_question_id": 0,
                    "seconds_since_issued": 0,
                    "select_count": 1,
                    "tested": 4,
                }
            ],
        },
    },
}

# test_project_server.py

import pytest
import datetime


def test_check_keys():
    from project_server import check_keys
    in_dict = {"color": "red",
               "shape": "round",
               "dimension": "3-D"}
    answer = check_keys(in_dict)
    expected = ["color", "shape", "dimension"]
    assert answer == expected

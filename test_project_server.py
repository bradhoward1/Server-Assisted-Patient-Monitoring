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


@pytest.mark.parametrize("result, expected",
                         [({"medical_record_number": 123,
                            "patient_name": "Brad_Howard",
                            "medical_image": "something.something",
                            "heart_rate": 55,
                            "ECG_image": "again.something"}, True),
                          ({"medical_record_number": "123",
                            "patient_name": "Brad_Howard",
                            "medical_image": "something.something",
                            "heart_rate": 55,
                            "ECG_image": "again.something"},
                              "There was an unacceptable input, try again"),
                          ({"medical_record_number": 123,
                            "heart_rate": 55,
                            "ECG_image": "again.something"}, True),
                          ({"medical_record_number": 123,
                            "patient_name": 22,
                            "medical_image": "something.something",
                            "heart_rate": 55,
                            "ECG_image": "again.something"},
                              "There was an unacceptable input, try again"),
                          ({"medical_record_number": 123,
                            "patient_name": "Brad_Howard",
                            "medical_image": 54,
                            "heart_rate": 55,
                            "ECG_image": "again.something"},
                              "There was an unacceptable input, try again"),
                          ({"medical_record_number": 123,
                            "patient_name": "Brad_Howard",
                            "medical_image": "something.something",
                            "heart_rate": "55",
                            "ECG_image": "again.something"},
                              "There was an unacceptable input, try again"),
                          ({"medical_record_number": "123",
                            "patient_name": "Brad_Howard",
                            "medical_image": "something.something",
                            "heart_rate": 55,
                            "ECG_image": 32},
                              "There was an unacceptable input, try again"),
                          ({"medical_record_number": "123",
                            "patient_name": "Brad_Howard",
                            "medical_image": "something.something",
                            "heart_rate": "55",
                            "ECG_image": "again.something"},
                              "There was an unacceptable input, try again")])
def test_validate_inputs(result, expected):
    from project_server import validate_inputs
    answer = validate_inputs(result)
    assert answer == expected


@pytest.mark.parametrize("result, expected",
                         [({"medical_record_number": 16,
                            "patient_name": "Brad",
                            "medical_image": "jpeg_image",
                            "ECG_image": "second_jpeg_image"}, True),
                          ({"medical_record_number": 16,
                            "medical_image": "jpeg_image",
                            "ECG_image": "second_jpeg_image"}, True)])
def test_add_new_patient_to_db(result, expected):
    from project_server import add_new_patient_to_db
    answer = add_new_patient_to_db(result)
    assert answer == expected


@pytest.mark.parametrize("result, expected",
                         [({"medical_record_number": 16,
                            "patient_name": "Brad",
                            "medical_image": "jpeg_image",
                            "ECG_image": "second_jpeg_image"}, True)])
def test_edit_existing_patient(result, expected):
    from project_server import edit_existing_patient
    answer = edit_existing_patient(result)
    assert answer == expected

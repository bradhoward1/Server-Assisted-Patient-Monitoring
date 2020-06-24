# test_project_server.py

import pytest
from datetime import datetime

pytest.global_variable_1 = ""


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
                            "heart_rate": 55,
                            "medical_image": "jpeg_image",
                            "ECG_image": "second_jpeg_image"}, True),
                          ({"medical_record_number": 17,
                            "medical_image": "jpeg_image",
                            "heart_rate": 67,
                            "ECG_image": "second_jpeg_image"}, True)])
def test_add_new_patient_to_db(result, expected):
    from project_server import add_new_patient_to_db
    answer = add_new_patient_to_db(result)
    assert answer == expected


@pytest.mark.parametrize("result, expected",
                         [({"medical_record_number": 16,
                            "patient_name": "Brad",
                            "heart_rate": 56,
                            "medical_image": "jpeg_image",
                            "ECG_image": "second_jpeg_image"}, True)])
def test_edit_existing_patient(result, expected):
    from project_server import edit_existing_patient
    answer = edit_existing_patient(result)
    assert answer == expected


@pytest.mark.parametrize("result, expected",
                         [(16, list)])
def test_timestamps_list(result, expected):
    from project_server import timestamps_list
    answer = timestamps_list(result)
    pytest.global_variable_1 = answer[0]
    answer = type(answer)
    assert answer == expected


@pytest.mark.parametrize("result, expected",
                         [(16, dict)])
def test_name_latest_hr_and_ECG_image(result, expected):
    from project_server import name_latest_hr_and_ECG_image
    answer = type(name_latest_hr_and_ECG_image(result))
    assert answer == expected


@pytest.mark.parametrize("result, expected",
                         [(16, list),
                          (17, list)])
def test_medical_image_list(result, expected):
    from project_server import medical_image_list
    answer = medical_image_list(result)
    answer = type(answer)
    assert answer == expected


@pytest.mark.parametrize("result, expected",
                         [({"patient": 12,
                            "timestamp": "2020-06-23 23:11:10"},
                           True),
                          ({"patient": "12",
                            "timestamp": "2020-06-23 23:11:10"},
                           "A valid patient id was not "
                           "provided, try again"),
                          ({"patient": 12,
                            "timestamp": 10},
                           "A valid timestamp was not "
                           "provided, try again"),
                          ({"patient": 12,
                            "timestamp": "2020-06-23 23:11:10",
                            "age": 10},
                           "The input dictionary has "
                           "unusable information, try again")])
def test_validate_ECG_image_timestamp(result, expected):
    from project_server import validate_ECG_image_timestamp
    answer = validate_ECG_image_timestamp(result)
    assert answer == expected


def test_ECG_image_timestamp():
    from project_server import ECG_image_timestamp
    in_dict = {"patient": 16,
               "timestamp": pytest.global_variable_1}
    answer = ECG_image_timestamp(in_dict)
    expected = "second_jpeg_image"
    assert answer == expected

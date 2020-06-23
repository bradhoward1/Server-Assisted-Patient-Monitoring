# client_test.py

import requests


out = {"medical_record_number": 100,
       "patient_name": "Brad",
       "medical_image": "jpeg_image",
       "heart_rate": 90,
       "ECG_image": "second_jpeg_image"}
r = requests.post("http://127.0.0.1:5000/add_new_patient", json=out)
print("{}, {}".format(r.text, r.status_code))


out = {"medical_record_number": 100,
       "patient_name": "Brad",
       "medical_image": "jpeg_image",
       "heart_rate": 90,
       "ECG_image": "second_jpeg_image"}
r = requests.post("http://127.0.0.1:5000/add_new_patient", json=out)
print("{}, {}".format(r.text, r.status_code))


out = {"medical_record_number": 102,
       "patient_name": "Brad",
       "medical_image": "jpeg_image",
       "heart_rate": 90,
       "ECG_image": "second_jpeg_image"}
r = requests.post("http://127.0.0.1:5000/add_new_patient", json=out)
print("{}, {}".format(r.text, r.status_code))


out = {"medical_record_number": 102,
       "patient_name": "Brad",
       "medical_image": "jpeg_image",
       "heart_rate": 90,
       "ECG_image": "second_jpeg_image"}
r = requests.post("http://127.0.0.1:5000/add_new_patient", json=out)
print("{}, {}".format(r.text, r.status_code))


out = {"medical_record_number": 102,
       "patient_name": "Brad",
       "medical_image": "jpeg_image",
       "heart_rate": 90,
       "ECG_image": "second_jpeg_image"}
r = requests.post("http://127.0.0.1:5000/add_new_patient", json=out)
print("{}, {}".format(r.text, r.status_code))


out = {"medical_record_number": 102,
       "patient_name": "Brad",
       "medical_image": "jpeg_image",
       "heart_rate": 90,
       "ECG_image": "second_jpeg_image"}
r = requests.post("http://127.0.0.1:5000/add_new_patient", json=out)
print("{}, {}".format(r.text, r.status_code))


out = {"medical_record_number": 102,
       "patient_name": "Brad",
       "medical_image": "jpeg_image",
       "heart_rate": 90,
       "ECG_image": "second_jpeg_image"}
r = requests.post("http://127.0.0.1:5000/add_new_patient", json=out)
print("{}, {}".format(r.text, r.status_code))


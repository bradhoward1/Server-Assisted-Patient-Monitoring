# client_test.py

import requests


host = "http://127.0.0.1:5000"

out = {"medical_record_number": 100,
       "patient_name": "Brad",
       "heart_rate": 90,
       "ECG_image": "second_jpeg_image"}
r = requests.post(host + "/add_new_patient", json=out)
print("{}, {}".format(r.text, r.status_code))


out = {"medical_record_number": 100,
       "patient_name": "Brad",
       "heart_rate": 170,
       "ECG_image": "foo"}
r = requests.post(host + "/add_new_patient", json=out)
print("{}, {}".format(r.text, r.status_code))


out = {"medical_record_number": 102,
       "patient_name": "Brad",
       "heart_rate": 90,
       "ECG_image": "second_jpeg_image"}
r = requests.post(host + "/add_new_patient", json=out)
print("{}, {}".format(r.text, r.status_code))


out = {"medical_record_number": 102,
       "patient_name": "Brad",
       "medical_image": "jpeg_image",
       "heart_rate": 90,
       "ECG_image": "second_jpeg_image"}
r = requests.post(host + "/add_new_patient", json=out)
print("{}, {}".format(r.text, r.status_code))


out = {"medical_record_number": 102,
       "patient_name": "Brad",
       "medical_image": "jpeg_image",
       "heart_rate": 90,
       "ECG_image": "second_jpeg_image"}
r = requests.post(host + "/add_new_patient", json=out)
print("{}, {}".format(r.text, r.status_code))


out = {"medical_record_number": 102,
       "patient_name": "Brad",
       "medical_image": "jpeg_image",
       "heart_rate": 90,
       "ECG_image": "second_jpeg_image"}
r = requests.post(host + "/add_new_patient", json=out)
print("{}, {}".format(r.text, r.status_code))


out = {"medical_record_number": 102,
       "patient_name": "Brad",
       "medical_image": "jpeg_image",
       "heart_rate": 170,
       "ECG_image": "foo"}
r = requests.post(host + "/add_new_patient", json=out)
print("{}, {}".format(r.text, r.status_code))


r = requests.get(host + "/name_hr_ecg/102")
print("{}, {}".format(r.text, r.status_code))

r = requests.get(host + "/name_hr_ecg/100")
print("{}, {}".format(r.text, r.status_code))


r = requests.get(host + "/ECG_timestamps/102")
print("{}, {}".format(r.text, r.status_code))


r = requests.get(host + "/medical_images/102")
print("{}, {}".format(r.text, r.status_code))

r = requests.get(host + "/medical_images/100")
print("{}, {}".format(r.text, r.status_code))


out = {"patient": 100,
       "timestamp": "2020-06-23 20:40:53"}
r = requests.post(host + "/ECG_image_timestamp", json=out)
print("{}, {}".format(r.text, r.status_code))

out = {"patient": "100",
       "timestamp": "2020-06-23 20:40:53"}
r = requests.post(host + "/ECG_image_timestamp", json=out)
print("{}, {}".format(r.text, r.status_code))

out = {"patient": 100,
       "timestamp": "2020-06-23 20:40:53",
       "whoops": "foo"}
r = requests.post(host + "/ECG_image_timestamp", json=out)
print("{}, {}".format(r.text, r.status_code))

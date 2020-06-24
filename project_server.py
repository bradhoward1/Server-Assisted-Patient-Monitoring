# project_server.py

from flask import Flask, request, jsonify
from datetime import datetime
from pymodm import connect, MongoModel, fields
import PIL

connect("mongodb+srv://brad_howard:NA@cluster0-lucsp.mongodb.net"
        "/another_rando?retryWrites=true&w=majority")


app = Flask(__name__)


class Patient(MongoModel):
    mr_number = fields.IntegerField(primary_key=True)
    name = fields.CharField()
    heart_rates = fields.ListField()
    medical_images = fields.ListField()
    ECG_images = fields.ListField()
    datetimes = fields.ListField()

# if __name__ == '__main__':
#     # u = Patient(mr_number=123, name="Brad",nums=[9])
#     # u.save()
#     bob=Patient.objects.raw({"_id": 123})
#     #bob = Patient()
#     #bob.mr_number = 5
#     # bob.save()
#     #print("bob is {}".format(bob_user))
#     bob.update({ "$push": { "nums": 77878 } } )
# #     # bob_user.save()
# #     ####pymodm.random_db.update({ "$push": { nums: { "$each":[90,92,85]}}})
# #     ####bob_user.save()


def __init__():
    print("Server is on.")


def add_new_patient_to_db(in_dict):
    new_patient = Patient()
    keys_present = check_keys(in_dict)
    for key in keys_present:
        if key == "medical_record_number":
            new_patient.mr_number = in_dict[key]
        elif key == "patient_name":
            new_patient.name = in_dict[key]
        elif key == "medical_image":
            new_patient.medical_images = [in_dict[key]]
        elif key == "heart_rate":
            new_patient.heart_rates = [in_dict[key]]
            recorded_datetime = datetime.now()
            string_recorded_datetime = datetime.strftime(
                    recorded_datetime,  "%Y-%m-%d %H:%M:%S")
            new_patient.datetimes = [string_recorded_datetime]
        elif key == "ECG_image":
            new_patient.ECG_images = [in_dict[key]]
        new_patient.save()
    return True


def edit_existing_patient(in_dict):
    keys_present = check_keys(in_dict)
    for key in keys_present:
        if key == "patient_name":
            existing_patient = Patient.objects.raw({"_id": in_dict
                                                    ["medical_record_number"]
                                                    }).first()
            existing_patient.name = in_dict["patient_name"]
            existing_patient.save()
        elif key == "medical_image":
            existing_patient = Patient.objects.raw({"_id": in_dict
                                                    ["medical_record_number"]
                                                    })
            existing_patient.update({"$push": {"medical_images":
                                    in_dict['medical_image']}})
        elif key == "heart_rate":
            existing_patient = Patient.objects.raw({"_id": in_dict
                                                    ["medical_record_number"]
                                                    })
            existing_patient.update({"$push": {"heart_rates":
                                    in_dict['heart_rate']}})
            recorded_datetime = datetime.now()
            string_recorded_datetime = datetime.strftime(
                    recorded_datetime,  "%Y-%m-%d %H:%M:%S")
            existing_patient.update({"$push":
                                    {"datetimes": string_recorded_datetime}})
        elif key == "ECG_image":
            existing_patient = Patient.objects.raw({"_id": in_dict
                                                    ["medical_record_number"]
                                                    })
            existing_patient.update({"$push": {"ECG_images":
                                    in_dict['ECG_image']}})
    return True


def check_keys(in_dict):
    my_keys = list(in_dict.keys())
    return my_keys


def validate_inputs(in_dict):
    keys_present = check_keys(in_dict)
    for key in keys_present:
        if key == "medical_record_number":
            if type(in_dict[key]) == int:
                continue
            else:
                return "There was an unacceptable input, try again"
        if key == "patient_name":
            if type(in_dict[key]) == str:
                continue
            else:
                return "There was an unacceptable input, try again"
        if key == "medical_image":
            if type(in_dict[key]) == str:
                continue
            else:
                return "There was an unacceptable input, try again"
        if key == "heart_rate":
            if type(in_dict[key]) == int:
                continue
            else:
                return "There was an unacceptable input, try again"
        if key == "ECG_image":
            if type(in_dict[key]) == str:
                continue
            else:
                return "There was an unacceptable input, try again"
    return True


@app.route("/add_new_patient", methods=["POST"])
def post_add_patient_to_db():
    in_dict = request.get_json()
    var = validate_inputs(in_dict)
    if var is True:
        try:
            presence_check = Patient.objects.get({"_id":
                                                 in_dict
                                                 ["medical_record_number"]})
        except Patient.DoesNotExist:
            presence_check = False
        if presence_check is not False:
            edit_existing_patient(in_dict)
            return "Good post made to database", 200
        else:
            add_new_patient_to_db(in_dict)
            return "Good new post made to database", 200

    else:
        return "Not an acceptable post, try again", 400


def patient_list():
    my_patient_list = list()
    for patient in Patient.objects.raw({}):
        my_patient_list.append(patient.mr_number)
    return my_patient_list


@app.route("/patient_list", methods=["GET"])
def get_patient_list():
    my_patient_list = get_patient_list()
    return jsonify(my_patient_lists), 200


def name_latest_hr_and_ECG_image(mr_num):
    mr_num = int(mr_num)
    patient = Patient.objects.raw({"_id": mr_num}).first()
    patient_name = patient.name
    patient_heart_rates = patient.heart_rates
    patient_ECG_images = patient.ECG_images
    size_of_hr_list = len(patient_heart_rates)
    size_of_patient_ECG_images = len(patient_ECG_images)
    latest_hr = patient_heart_rates[size_of_hr_list-1]
    latest_ECG_image = patient_ECG_images[size_of_patient_ECG_images-1]
    out_dict = {"name": patient_name,
                "latest_hr": latest_hr,
                "latest_ECG_image": latest_ECG_image}
    return out_dict


@app.route("/name_hr_ecg/<mr_num>", methods=["GET"])
def get_name_latest_hr_and_ECG_image(mr_num):
    contents = name_latest_hr_and_ECG_image(mr_num)
    if contents:
        return jsonify(contents), 200
    else:
        return "Unable to return the contents, try again", 400


def timestamps_list(mr_num):
    mr_num = int(mr_num)
    patient = Patient.objects.raw({"_id": mr_num}).first()
    patient_timestamp_list = patient.datetimes
    return patient_timestamp_list


@app.route("/ECG_timestamps/<mr_num>", methods=["GET"])
def get_timestamps_list(mr_num):
    contents = timestamps_list(mr_num)
    if contents:
        return jsonify(contents), 200
    else:
        return "Unable to retrieve list of timestamps", 400


def medical_image_list(mr_num):
    mr_num = int(mr_num)
    patient = Patient.objects.raw({"_id": mr_num}).first()
    patient_image_list = patient.medical_images
    return patient_image_list


if __name__ == '__main__':
    __init__()
    app.run()
    # patient_list()

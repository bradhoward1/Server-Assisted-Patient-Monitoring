# project_server.py

from flask import Flask, request, jsonify
from datetime import datetime
from pymodm import connect, MongoModel, fields
import PIL

connect("mongodb+srv://brad_howard:NA@cluster0-"
        "lucsp.mongodb.net/random_db?retryWrites=true&w=majority")


app = Flask(__name__)


class Patient(MongoModel):
    mr_number = fields.IntegerField(primary_key=True)
    name = fields.CharField()
    heart_rates = fields.ListField()
    medical_image = fields.CharField()
    ECG_image = fields.CharField()
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
            new_patient.medical_image = in_dict[key]
        elif key == "heart_rate":
            new_patient.heart_rates = [in_dict[key]]
            recorded_datetime = datetime.now()
            string_recorded_datetime = datetime.strftime(
                    recorded_datetime,  "%Y-%m-%d %H:%M:%S")
            new_patient.datetimes = [string_recorded_datetime]
        elif key == "ECG_image":
            new_patient.ECG_image = in_dict[key]
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
                                                    }).first()
            existing_patient.medical_image = in_dict[key]
            existing_patient.save()
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
                                                    }).first()
            existing_patient.ECG_image = in_dict[key]
            existing_patient.save()
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

if __name__ == '__main__':
    __init__()
    app.run()

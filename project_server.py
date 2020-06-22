# project_server.py

from flask import Flask, request, jsonify
from datetime import datetime
from pymodm import connect, MongoModel, fields
import PIL

# connect("mongodb+srv://brad_howard:NA@cluster0-lucsp.mongodb.net/random_db?retryWrites=true&w=majority")


# if __name__ == '__main__':
#     u = Patient(mr_number=123, name="Brad",nums=[9])
#     u.save()
#     bob=Patient.objects.raw({"_id": 123})
#     bob.update({ "$push": { "nums": { "$each": [ 90, 92, 85, 20 ] } } })
#     ####pymodm.random_db.update({ "$push": { nums: { "$each":[90,92,85]}}})
#     ####bob_user.save()

app = Flask(__name__)


class Patient(MongoModel):
    mr_number = fields.IntegerField(primary_key=True)
    name = fields.CharField()
    heart_rates = fields.ListField()
    medical_image = fields.ImageField()
    ECG_image = fields.ImageField()
    datetimes = fields.ListField()


def add_patient_to_db():
    pass


def check_keys(in_dict):
    my_keys = list(in_dict.keys())
    return my_keys


def validate_inputs():
    pass


@app.route("/add_new_patient", methods=["POST"])
def post_add_patient_to_db():
    pass

if __name__ == '__main__':
    check_keys({"blue": 1,
                "red": 2})

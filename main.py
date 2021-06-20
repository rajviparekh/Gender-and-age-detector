import os
from uuid import uuid4
from flask import Flask, request, render_template, send_from_directory
import numpy as np
import cv2
import detection
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


model = r'detection.py'
model = os.path.join(os.path.dirname(__file__),model)

if not os.path.isfile(model):
    print("model is missing from the model folder")
    exit()



@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')

    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    

    for upload in request.files.getlist("file"):
        filename = upload.filename
        destination = "/".join([target, filename])
        upload.save(destination)

    if request.method=='POST':
        input = cv2.imread(destination)
        gender, age = detection.age_gender_detector(input)
        return render_template("result.html", gender=gender, age=age)


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, jsonify, request
import os
from PIL import Image
import tensorflow as tf
import numpy as np

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def base_url():
    return jsonify({
        "status":"OK",
        "message":"API berhasil terhubung"
    }), 200

@app.route("/", methods=["POST"])
def clasify_image():
    if "file" not in request.files:
        return jsonify({
            "status": "Bad Request",
            "message": "No file part."
        }), 400

    source_file_name = request.files.get("file")
    

    if source_file_name.filename == "":
        return jsonify({
            "status": "Bad Request",
            "message": "No selected file."
        }), 400

    if not (source_file_name and allowed_file(source_file_name.filename)):
        return jsonify({
            "status": "Not Acceptable",
            "message": "Only files with extension png, jpg, jpeg are allowed."
        }), 406
        
    img = Image.open(source_file_name)
    img = img.resize((255,255),Image.ANTIALIAS)
    img = np.asarray(img)
    list_image = []
    list_image.append(img)
    list_image = np.asarray(list_image)
    print(list_image.shape)
    # feature = read_and_process_image(img)
    model = tf.keras.models.load_model("./models/23082022-model_new.h5")
    predictions = model.predict(list_image)
    jenis = 0
    keterangan = ""
    if predictions >= 0.5:
        jenis = 1
        keterangan = "non-fire"
    else:
        jenis = 0
        keterangan = "fire"

    return jsonify({
            "status": "OK",
            "message": "Hope The data received well.",
            "value_pred":str(predictions[0][0]),
            "jenis":str(jenis),
            "keterangan":keterangan
        }), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
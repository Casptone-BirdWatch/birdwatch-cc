from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Load model TFLite
interpreter = tf.lite.Interpreter(model_path="model-burung.tflite")  # Pastikan path dan nama file benar
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load class list from file
with open('class_list.txt', 'r') as f:
    class_list = [line.strip() for line in f]

# Dictionary untuk deskripsi burung
bird_descriptions = {
    "BURUNG CENDERAWASIH BOTAK": {
        "deskripsi": "Cenderawasih botak atau dalam nama ilmiahnya Cicinnurus respublica adalah sejenis burung pengicau berukuran kecil, dari marga Cicinnurus. Burung jantan dewasa memiliki bulu berwarna merah dan hitam dengan tengkuk berwarna kuning, mulut hijau terang, kaki berwarna biru dan dua bulu ekor ungu melingkar. Kulit kepalanya berwarna biru muda terang dengan pola salib ganda hitam. Burung betina berwarna coklat dengan kulit kepala biru muda.",
        "famili": "Paradisaeidae",
        "genus": "Cicinnurus"
    },
    "BURUNG KUAU KERDIL KALIMANTAN": {
        "deskripsi": "Kuau-kerdil Kalimantan atau dalam nama ilmiahnya Polyplectron schleiermacheri adalah jenis kuau-kerdil berukuran sedang yang berhabitat di hutan hujan dataran rendah Pulau Kalimantan. Kuau ini adalah jenis kuau merak yang paling langka dan sudah jarang ditemui. Cirinya adalah ukuran tubuhnya yang maksimal dapat tumbuh sampai 50 cm dengan bintik-bintik pada tubuhnya. Kuau merak Kalimantan masih berkerabat dengan kuau-kerdil Malaya dan kuau-kerdil Palawan.",
        "famili": "Phasianidae",
        "genus": "Polyplectron"
    },
    "BURUNG CICA DAUN KALIMANTAN": {
        "deskripsi": "Deskripsi untuk Burung Cica Daun Kalimantan belum tersedia.",
        "famili": "Cycadaceae",
        "genus": "Cycas"
    },
    "BURUNG JALAK BALI": {
        "deskripsi": "Deskripsi untuk Burung Jalak Bali belum tersedia.",
        "famili": "Sturnidae",
        "genus": "Leucopsar"
    },
    "BURUNG JUNAI EMAS": {
        "deskripsi": "Deskripsi untuk Burung Junai Emas belum tersedia.",
        "famili": "Columbidae",
        "genus": "Chalcophaps"
    },
    "BURUNG MALEO": {
        "deskripsi": "Deskripsi untuk Burung Maleo belum tersedia.",
        "famili": "Megapodiidae",
        "genus": "Macrocephalon"
    },
    "BURUNG PENCUK ULAR ASIA": {
        "deskripsi": "Deskripsi untuk Burung Pencuk Ular Asia belum tersedia.",
        "famili": "Cuculidae",
        "genus": "Hierococcyx"
    },
    "BURUNG SEMPIDAN KALIMANTAN": {
        "deskripsi": "Deskripsi untuk Burung Sempidan Kalimantan belum tersedia.",
        "famili": "Bucerotidae",
        "genus": "Anthracoceros"
    },
    "BURUNG SEMPUR HUJAN DARAT": {
        "deskripsi": "Deskripsi untuk Burung Sempur Hujan Darat belum tersedia.",
        "famili": "Pycnonotidae",
        "genus": "Pycnonotus"
    },
    "BURUNG TIONG BATU KALIMANTAN": {
        "deskripsi": "Deskripsi untuk Burung Tiong Batu Kalimantan belum tersedia.",
        "famili": "Sturnidae",
        "genus": "Gracula"
    }
}

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Preprocess the image
        image = Image.open(io.BytesIO(file.read())).resize((416, 416))  # Adjust target size
        image = np.array(image, dtype=np.float32) / 255.0  # Normalize the image
        image = np.expand_dims(image, axis=0)  # Add batch dimension

        # Set input tensor
        interpreter.set_tensor(input_details[0]['index'], image)
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])

        # Find the index of the maximum value in the predictions
        predicted_class_index = np.argmax(predictions[0])
        if predicted_class_index >= len(class_list) or predicted_class_index < 0:
            return jsonify({'error': 'Kesalahan dalam prediksi, mohon coba foto lain'}), 400

        predicted_class = class_list[predicted_class_index]

        # Get description
        description_data = bird_descriptions.get(predicted_class, {"deskripsi": "Deskripsi tidak tersedia"})
        result = {
            'Jenis Burung': predicted_class,
            'Deskripsi': description_data.get("deskripsi"),
            'Famili': description_data.get("famili", "Tidak diketahui"),
            'Genus': description_data.get("genus", "Tidak diketahui")
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
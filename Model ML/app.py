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
        "deskripsi": "Burung Cica Daun Kalimantan, dikenal dengan nama ilmiah Chloropsis cyanopogon, adalah burung berukuran kecil hingga sedang dengan bulu berwarna hijau cerah yang mencolok, disertai dengan aksen warna biru dan kuning di beberapa bagian tubuh. Burung ini memiliki paruh hitam yang tajam dan melengkung, cocok untuk memakan serangga, buah-buahan, dan nektar. Burung Cica Daun Kalimantan adalah penghuni hutan-hutan tropis dan subtropis di dataran rendah Kalimantan, Sumatra, dan Semenanjung Malaya. Kicauannya merdu dan variatif, sering digunakan untuk komunikasi antarindividu, terutama pada musim kawin. Meskipun menghadapi ancaman dari perusakan habitat dan perdagangan burung liar, spesies ini belum termasuk dalam kategori terancam punah menurut IUCN.",
        "famili": "Chloropseidae",
        "genus": "Chloropsis"
    },
    "BURUNG JALAK BALI": {
        "deskripsi": "Burung Jalak Bali, dikenal dengan nama ilmiah Leucopsar rothschildi, adalah burung endemik dari Bali, Indonesia. Burung ini memiliki penampilan yang sangat mencolok dengan bulu berwarna putih bersih, ujung sayap dan ekor berwarna hitam, serta kulit sekitar mata yang berwarna biru cerah. Burung Jalak Bali memiliki paruh kuning keabu-abuan dan kaki berwarna abu-abu. Burung ini biasanya ditemukan di hutan mangrove dan kawasan hutan lainnya di Bali. Mereka memakan berbagai jenis makanan seperti serangga, buah-buahan, dan biji-bijian. Kicauan Jalak Bali terdiri dari suara yang bervariasi, termasuk siulan dan panggilan yang keras. Burung ini termasuk dalam kategori sangat terancam punah menurut IUCN, terutama karena perburuan liar dan hilangnya habitat. Upaya konservasi yang ketat sedang dilakukan untuk melindungi dan meningkatkan populasi mereka di alam liar.",
        "famili": "Sturnidae",
        "genus": "Leucopsar"
    },
    "BURUNG JUNAI EMAS": {
        "deskripsi": "Burung Junai Emas, dikenal dengan nama ilmiah Caloenas nicobarica, adalah salah satu spesies burung merpati yang menonjol dengan bulu yang sangat indah dan unik. Burung ini memiliki bulu tubuh berwarna hijau metalik dengan kilauan emas dan tembaga, yang membuatnya terlihat sangat menarik di bawah sinar matahari. Bagian lehernya dihiasi dengan bulu-bulu panjang yang menjuntai, memberikan penampilan yang anggun. Ekor burung ini berwarna putih, yang kontras dengan warna tubuhnya yang gelap. Junai Emas biasanya ditemukan di hutan-hutan tropis dan subtropis di kepulauan Nicobar, Andaman, dan beberapa pulau di kawasan Asia Tenggara, termasuk Indonesia dan Filipina. Mereka sering memakan buah-buahan, biji-bijian, dan serangga kecil. Burung ini berperan penting dalam ekosistem sebagai penyebar biji-bijian, membantu regenerasi hutan. Meskipun belum masuk dalam kategori terancam punah, populasi Junai Emas terancam oleh perusakan habitat dan perburuan liar.",
        "famili": "Columbidae",
        "genus": "Caloenas"
    },
    "BURUNG MALEO": {
        "deskripsi": "Burung Maleo, dengan nama ilmiah Macrocephalon maleo, adalah burung endemik Sulawesi yang terkenal dengan kebiasaannya bertelur di tanah panas atau di dekat sumber panas bumi. Burung ini memiliki tubuh berwarna hitam dan putih, dengan wajah merah jambu dan paruh kuning. Betina menggali lubang di pasir pantai atau tanah vulkanik untuk bertelur, dan telur-telur tersebut diinkubasi oleh panas dari matahari atau sumber panas bumi. Anak burung Maleo yang baru menetas dapat terbang dan hidup mandiri segera setelah keluar dari telur. Populasi burung ini terancam oleh perusakan habitat dan pengambilan telur secara ilegal.",
        "famili": "Megapodiidae",
        "genus": "Macrocephalon"
    },
    "BURUNG PENCUK ULAR ASIA": {
        "deskripsi": "Burung Pencuk Ular Asia, dikenal dengan nama ilmiah Anhinga melanogaster, adalah burung air yang tersebar luas di Asia Selatan dan Asia Tenggara. Burung ini memiliki leher yang panjang dan ramping, mirip dengan ular, serta tubuh berwarna gelap dengan kilauan metalik. Mereka biasanya ditemukan di danau, sungai, dan rawa, di mana mereka berburu ikan dengan menyelam dan menggunakan lehernya yang panjang untuk menangkap mangsa. Setelah berburu, mereka sering terlihat berjemur dengan sayap terbuka untuk mengeringkan bulu mereka.",
        "famili": "Anhingidae",
        "genus": "Anhinga"
    },
    "BURUNG SEMPIDAN KALIMANTAN": {
        "deskripsi": "Burung Sempidan Kalimantan, atau dikenal dengan nama ilmiah Lophura bulweri, adalah burung yang endemik di hutan-hutan tropis Kalimantan. Burung ini memiliki bulu yang indah dengan warna dominan biru metalik dan putih. Burung jantan memiliki ekor panjang yang menjuntai dan bulu hiasan di kepala yang berwarna cerah, sedangkan betina memiliki bulu yang lebih kusam. Mereka hidup di hutan primer dan mencari makan di lantai hutan berupa biji-bijian, serangga, dan buah-buahan.",
        "famili": "Phasianidae",
        "genus": "Lophura"
    },
    "BURUNG SEMPUR HUJAN DARAT": {
        "deskripsi": "Burung Sempur Hujan Darat, dikenal dengan nama ilmiah Scissirostrum dubium, adalah burung yang ditemukan di Sulawesi. Burung ini memiliki bulu berwarna abu-abu dengan bagian kepala berwarna hitam mengilap. Mereka hidup berkelompok dan sering ditemukan di hutan-hutan dan lahan pertanian, di mana mereka mencari makan berupa serangga dan buah-buahan. Burung ini dikenal karena kebiasaan bersarangnya yang unik, di mana mereka membuat sarang dari ranting-ranting yang ditempatkan di pohon-pohon besar.",
        "famili": "Sturnidae",
        "genus": "Scissirostrum"
    },
    "BURUNG TIONG BATU KALIMANTAN": {
        "deskripsi": "Burung Tiong Batu Kalimantan, atau dikenal dengan nama ilmiah Pityriasis gymnocephala, adalah burung yang endemik di Kalimantan. Burung ini memiliki penampilan yang unik dengan kepala botak berwarna merah cerah dan bulu tubuh yang hitam. Mereka hidup di hutan-hutan tropis dataran rendah dan hutan pegunungan, di mana mereka memakan serangga, buah-buahan, dan biji-bijian. Burung ini sering ditemukan dalam kelompok kecil dan terkenal karena suaranya yang keras dan berisik.",
        "famili": "Pityriaseidae",
        "genus": "Pityriasis"
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

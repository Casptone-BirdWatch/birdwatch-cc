const express = require('express');
const multer = require('multer');
const axios = require('axios');
const { db, bucket } = require('./firebaseConfig');
const FormData = require('form-data');
const admin = require('firebase-admin');

const app = express();
const port = process.env.PORT || 3000;

const upload = multer({ storage: multer.memoryStorage() });

// Middleware untuk parsing JSON
app.use(express.json());

// Middleware untuk memverifikasi token ID Firebase
const verifyToken = async (req, res, next) => {
  const idToken = req.headers.authorization && req.headers.authorization.split('Bearer ')[1];
  
  if (!idToken) {
    return res.status(403).send('No token provided');
  }

  try {
    const decodedToken = await admin.auth().verifyIdToken(idToken);
    req.user = decodedToken;
    next();
  } catch (error) {
    console.error(error);
    res.status(403).send('Unauthorized');
  }
};

// Route untuk prediksi burung
app.post('/predict', verifyToken, upload.single('image'), async (req, res) => {
  if (!req.file) {
    return res.status(400).send('No file uploaded.');
  }

  try {
    const blob = bucket.file(Date.now() + '-' + req.file.originalname);
    const blobStream = blob.createWriteStream({
      metadata: {
        contentType: req.file.mimetype,
      },
    });

    blobStream.end(req.file.buffer);
    const publicUrl = `https://storage.googleapis.com/${bucket.name}/${blob.name}`;

    const form = new FormData();
    form.append('file', req.file.buffer, {
      filename: req.file.originalname,
      contentType: req.file.mimetype,
    });

    const response = await axios.post('https://model-ml-kuidm4znma-et.a.run.app/predict', form, {
      headers: form.getHeaders(),
    });

    const { 'Jenis Burung': JenisBurung, Deskripsi, Famili, Genus } = response.data;

    if (!JenisBurung || !Deskripsi || !Famili || !Genus) {
      return res.status(500).send('Invalid response from prediction model');
    }

    // Simpan hasil prediksi ke Firestore tanpa imageUrl
    const userId = req.user.uid;
    const docRef = await db.collection('predictions').add({
      userId,
      JenisBurung,
      Deskripsi,
      Famili,
      Genus,
      timestamp: admin.firestore.FieldValue.serverTimestamp(),
    });

     // Mengembalikan respons dengan imageUrl
    res.status(200).json({
      id: docRef.id,
      JenisBurung,
      Deskripsi,
      Famili,
      Genus,
      imageUrl: publicUrl,
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Internal server error');
  }
});

// Route untuk menambahkan bookmark
app.post('/bookmark', verifyToken, async (req, res) => {
  const { predictionId } = req.body;
  const userId = req.user.uid;

  try {
    const predictionRef = db.collection('predictions').doc(predictionId);
    const predictionSnapshot = await predictionRef.get();

    if (!predictionSnapshot.exists) {
      return res.status(404).send('Prediction not found.');
    }

    const predictionData = predictionSnapshot.data();
    const { JenisBurung, Deskripsi, Famili, Genus, imageUrl } = predictionData;

    const docRef = await db.collection('bookmarks').add({
      userId,
      prediction: { JenisBurung, Deskripsi, Famili, Genus },
      imageUrl,
      timestamp: admin.firestore.FieldValue.serverTimestamp(),
    });

    res.status(200).send({ id: docRef.id, message: 'Bookmark added' });
  } catch (error) {
    console.error(error);
    res.status(500).send('Internal server error');
  }
});

// Route untuk menghapus bookmark
app.delete('/bookmark/:id', verifyToken, async (req, res) => {
  const bookmarkId = req.params.id;

  try {
    await db.collection('bookmarks').doc(bookmarkId).delete();

    res.status(200).send('Bookmark deleted');
  } catch (error) {
    console.error(error);
    res.status(500).send('Internal server error');
  }
});

// Start server
app.listen(port, () => {
  console.log(`BirdWatch is running on port ${port}`);
});
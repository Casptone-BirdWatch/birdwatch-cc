# Deploying the ML Model 🚀

Hey there! Ready to get this ML model up and running? Follow these simple steps to deploy like a pro.

## Step 1: Clone the Repository
First things first, clone this repo to your local machine:
```bash
git clone https://github.com/Casptone-BirdWatch/birdwatch-cc.git
cd birdwatch-cc/Model\ ML
```

## Step 2: Download the ML Model
Grab the .tflite model from this [Google Drive](https://drive.google.com/drive/folders/1LipUDJ3KZ6ZBwMqKyz2PoUupqzTRI6AR?usp=sharing). Save it in the Model ML directory.

## Step 3: Deploy with gcloud
Open your terminal, navigate to the project folder, and deploy using this command:
```bash
gcloud run deploy --source . --port 3000
```

And that's it! Your ML model should be up and running. Happy deploying! 🚀

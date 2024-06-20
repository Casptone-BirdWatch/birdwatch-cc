# Deploying the Backend 🚀

Hey there! Ready to deploy your backend service? Follow these steps to get started!

## Step 1: Clone the Repository
First, clone this repository to your local machine:
```bash
git clone https://github.com/Casptone-BirdWatch/birdwatch-cc.git
cd birdwatch-cc/Backend
```

## Step 2: Link the ML Model Deployment to index.js
Insert the deployment link of your ML model into the index.js file.

## Step 3: Create a Google Cloud Service Account Key
Generate a service account key for your Google Cloud project.

## Step 4: Deploy with gcloud
Open your terminal, navigate to the project folder, and deploy your backend using this command:
```bash
gcloud run deploy --source . --port 3000
```

And that's it! Your backend should be deployed and ready to go 🚀

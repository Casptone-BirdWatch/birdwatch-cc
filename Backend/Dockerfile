# Gunakan image Node.js
FROM node:16

# Set working directory
WORKDIR /usr/src/app

# Salin file package.json dan package-lock.json untuk instalasi dependensi
COPY package*.json ./

# Install dependensi
RUN npm install

# Salin kode aplikasi Anda ke dalam image Docker
COPY . .

# Port yang akan diexpose oleh aplikasi
EXPOSE 3000

# Perintah untuk menjalankan aplikasi
CMD ["node", "index.js"]
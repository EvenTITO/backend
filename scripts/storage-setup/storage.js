const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');


async function upload(url, filename) {
  const filePath = path.join(__dirname, filename);
  const fileStream = fs.createReadStream(filePath);

  const response = await fetch(url, {
      method: 'PUT',
      headers: {
          'Content-Type': 'image/png'
      },
      body: fileStream
  });
}


upload('https://storage.googleapis.com/PATH-AL-STORAGE-CON-WRITE-PERMISSIONS-CREADO-CON-SIGNEDURL', 'image.png').then(

  console.log('Ejecuto bien')
)


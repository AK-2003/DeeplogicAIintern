const express = require('express');
const multer = require('multer');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const upload = multer({ dest: 'uploads/' });

app.set('view engine', 'ejs');

app.get('/', (req, res) => {
  res.render('index');
});

app.post('/upload', upload.single('pdf_file'), (req, res) => {
  if (!req.file) {
    return res.send('No file uploaded');
  }

  const filePath = req.file.path;
  const fileExtension = path.extname(req.file.originalname);
  const uploadedFileName = req.file.filename + fileExtension;
  const newFilePath = path.join(req.file.destination, uploadedFileName);

  // Rename the file
  fs.renameSync(filePath, newFilePath);

  // Run the extraction script
  const extractionProcess = spawn('python', ['1.py', newFilePath]);

  let extractedData = '';

  extractionProcess.stdout.on('data', (data) => {
    extractedData += data.toString('utf-8');
  });

  extractionProcess.stderr.on('data', (data) => {
    console.error(`Extraction process error: ${data}`);
  });

  extractionProcess.on('close', (code) => {
    if (code === 0) {
      res.render('result', { data: extractedData });
    } else {
      res.render('result', { data: 'Extraction failed' });
    }
  });
});

app.listen(4000, () => {
  console.log('Server started on port 4000');
});

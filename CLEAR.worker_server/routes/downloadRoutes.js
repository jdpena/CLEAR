// XXX A. XXX. Distribution is unlimited.

// XXX supported XXXnder XXX of XXX for 
// XXX and XXX under XXX Contract No. XXX-15-D-XXX. Any opinions,
// findings, XXX 
// of the author(s) XXX the XXX 
// XXX of XXX for XXX and XXX.

// © 2023 XXX.

// XXX.XXX-11 Patent Rights - XXX (May 2014)

// The software/XXX-Is basis

// XXX.S. XXX with Unlimited Rights, as defined in XXX Part 
// XXX.XXX-XXX or 7014 (Feb 2014). Notwithstanding any copyright notice, 
// U.S. XXX rights in this work are defined by XXX XXX.XXX-XXX or 
// XXX XXX.XXX-7014 as detailed above. Use of this work other than as specifically
// XXX XXX.S. XXX may violate any copyrights that exist in this work.

const express = require('express');
const fs = require('fs');
const path = require('path');
const multer = require('multer');
const router = express.Router();

// Create the storage folder if it doesn't exist
const storageFolder = path.join(__dirname, '../storage');
if (!fs.existsSync(storageFolder)) {
  fs.mkdirSync(storageFolder);
}

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, storageFolder);
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  }
});

const upload = multer({
  storage: storage,
  limits: {
    fileSize: 1024 * 1024 * 1024 * 10 // Limited to 10GB
  }
});

module.exports = function(io) {
  // Check if a file exists
  router.get('/exists/:filename', (req, res) => {
    const fileName = req.params.filename;
    const filePath = path.join(storageFolder, fileName);

    fs.access(filePath, fs.constants.F_OK, (err) => {
      if (err) {
        res.status(404).send('File not found');
        return;
      }
      res.status(200).send('File exists');
    });
  });

  // For downloading a file
  router.get('/download/:filename', (req, res) => {
    const fileName = req.params.filename;
    const filePath = path.join(storageFolder, fileName);

    fs.access(filePath, fs.constants.F_OK, (err) => {
      if (err) {
        res.status(404).send('File not found');
        return;
      }

      const stat = fs.statSync(filePath);

      res.writeHead(200, {
        'Content-Type': 'application/octet-stream',
        'Content-Length': stat.size,
        'Content-Disposition': `attachment; filename=${path.basename(filePath)}`
      });

      const readStream = fs.createReadStream(filePath);
      readStream.pipe(res);
    });
  });

  // Upload file
  router.post('/upload', upload.single('file'), (req, res) => {
    if (!req.file) {
      return res.status(400).send('No file uploaded');
    }

    const filePath = req.file.path;

    res.status(200).send(`File uploaded to ${filePath}`);
  });

  return router;
};

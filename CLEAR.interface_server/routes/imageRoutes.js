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
const router = express.Router();
const bodyParser = require('body-parser');

module.exports = function (io) {
  let image = null;
  const jsonParser = bodyParser.json();
  const urlencodedParser = bodyParser.urlencoded({ extended: true });

  const processImage = (img_base64, req, res) => {
    image = img_base64;
    io.emit('image_updated', 'A new image has been uploaded.');
    res.status(200).json({ status: 'success', message: 'Image uploaded and saved to a variable.' });
  };

  router.post('/unityimage', [jsonParser, urlencodedParser], (req, res) => {
    const img_base64 = req.body.image;
    processImage(img_base64, req, res);
  });

  router.post('/image', jsonParser, (req, res) => {
    const img_base64 = req.body.image;
    processImage(img_base64, req, res);
  });
  
  router.get('/image', (req, res) => {
    if (image) {
      const imgBuffer = Buffer.from(image, 'base64');
      res.type('image/webp').send(imgBuffer);
    } else {
      res.status(404).json({ status: 'error', message: 'No image found' });
    }
  });

  router.get('/webImage', (req, res) => {
    if (image) {
      res.status(200).json({ status: 'success', image });
    } else {
      res.status(404).json({ status: 'error', message: 'No image found' });
    }
  });

  return router;
};

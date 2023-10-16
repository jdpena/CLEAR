const express = require('express');
const router = express.Router();

module.exports = function (io) {
  let objectImage = null;
  let depthImage = null;

  router.post('/image', (req, res) => {
    const img_base64 = req.body.image;

    objectImage = img_base64;
    depthImage = img_base64;

    io.emit('image_updated', 'A new image has been uploaded.');

    res.status(200).json({ status: 'success', message: 'Image uploaded and saved to a variable.' });
  });

  router.get('/objectImage', (req, res) => {
    let tempImage = objectImage
    objectImage = null;
    if (tempImage) {
      const imgBuffer = Buffer.from(tempImage, 'base64');
      res.type('image/webp').send(imgBuffer); // Changed the response type to 'image/webp'
    } else {
      res.status(404).json({ status: 'error', message: 'No image found' });
    }
  });

  router.get('/depthImage', (req, res) => {
    let tempImage = depthImage
    depthImage = null;
    if (tempImage) {
      const imgBuffer = Buffer.from(tempImage, 'base64');
      res.type('image/webp').send(imgBuffer);
    } else {
      res.status(404).json({ status: 'error', message: 'No image found' });
    }
  });

  return router;
};

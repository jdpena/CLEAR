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
  let unityimage = null;

  router.use(bodyParser.json());
  router.use(bodyParser.urlencoded({ extended: true }));

  router.post('/unityimage', (req, res) => {
    const img_base64 = req.body.image;
    unityimage = img_base64;
    if (unityimage) {
      io.emit('unity_image_updated', 'A new image has been uploaded.');
    }
    res.status(200).json({ status: 'success', message: 'Image uploaded and saved to a variable.' });
  });

  router.get('/unityimage', (req, res) => {
    let tempImage = unityimage;
    // image = null;
    if (tempImage) {
      const imgBuffer = Buffer.from(tempImage, 'base64');
      res.type('image/jpeg').send(imgBuffer); // Changed the response type to 'image/jpeg'
    } else {
      res.status(404).json({ status: 'error', message: 'No image found' });
    }
  });
  return router;
};

// DISTRIBUTION STATEMENT A. Approved for public release. Distribution is unlimited.

// This material is based upon work supported by the Under Secretary of Defense for 
// Research and Engineering under Air Force Contract No. FA8702-15-D-0001. Any opinions,
// findings, conclusions or recommendations expressed in this material are those 
// of the author(s) and do not necessarily reflect the views of the Under 
// Secretary of Defense for Research and Engineering.

// © 2023 Massachusetts Institute of Technology.

// Subject to FAR52.227-11 Patent Rights - Ownership by the contractor (May 2014)

// The software/firmware is provided to you on an As-Is basis

// Delivered to the U.S. Government with Unlimited Rights, as defined in DFARS Part 
// 252.227-7013 or 7014 (Feb 2014). Notwithstanding any copyright notice, 
// U.S. Government rights in this work are defined by DFARS 252.227-7013 or 
// DFARS 252.227-7014 as detailed above. Use of this work other than as specifically
// authorized by the U.S. Government may violate any copyrights that exist in this work.

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

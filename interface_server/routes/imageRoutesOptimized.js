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
const sharp = require('sharp');
const router = express.Router();
const bodyParser = require('body-parser');
const ImageBuffer = require('../VisualSupport/ImageBuffer');

module.exports = function (io) {
  let image = null;
  const jsonParser = bodyParser.json();
  const urlencodedParser = bodyParser.urlencoded({ extended: true });

  const processImage = async (imgBuffer, req, res) => {
    try {
        const imageBufferInstance = new ImageBuffer(imgBuffer);
        
        const width = imageBufferInstance.width;
        const height = imageBufferInstance.height;
        // Since the image data is now in a matrix, if you need the flat RGB array, 
        // you'd have to reconstruct it from the matrix. 
        // For the purpose of this example, I'm still using the sliced buffer.

        const rgbData = imgBuffer.slice(8);

        // Convert the byte stream to webp format
        const webpBuffer = await sharp(rgbData, {
            raw: {
                width: width,
                height: height,
                channels: 3
            }
        })
        .webp()
        .toBuffer();

        image = webpBuffer; // Saving the converted image to the global variable.

        io.emit('image_updated', 'A new image has been uploaded.');
        res.status(200).json({ status: 'success', message: 'Image uploaded and converted to WebP format.' });
    } catch (err) {
        console.error("Error converting to WebP:", err);
        res.status(500).json({ status: 'error', message: 'Error processing the image.' });
    }
  };

  router.post('/unityimage', (req, res) => {
      let chunks = [];
      req.on('data', chunk => {
          chunks.push(chunk);
      });
      req.on('end', async () => {
          // Now we have the raw bytes of the image
          const imgData = Buffer.concat(chunks);
          await processImage(imgData, req, res);
      });
  });

  router.post('/image', jsonParser, (req, res) => {
    const img_base64 = req.body.image;
    processImage(img_base64, req, res);
  });
  
  router.get('/image', (req, res) => {
    if (image) {
      res.type('image/webp').send(image);
    } else {
      res.status(404).json({ status: 'error', message: 'No image found' });
    }
});


  router.get('/webImage', (req, res) => {
    if (image) {
      res.status(200).json({ status: 'success', image: image.toString('base64') });
    } else {
      res.status(404).json({ status: 'error', message: 'No image found' });
    }
  });


  return router;
};

# XXX A. XXX. Distribution is unlimited.

# XXX supported XXXnder XXX of XXX for 
# XXX and XXX under XXX Contract No. XXX-15-D-XXX. Any opinions,
# findings, XXX 
# of the author(s) XXX the XXX 
# XXX of XXX for XXX and XXX.

# © 2023 XXX.

# XXX.XXX-11 Patent Rights - XXX (May 2014)

# The software/XXX-Is basis

# XXX.S. XXX with Unlimited Rights, as defined in XXX Part 
# XXX.XXX-XXX or 7014 (Feb 2014). Notwithstanding any copyright notice, 
# U.S. XXX rights in this work are defined by XXX XXX.XXX-XXX or 
# XXX XXX.XXX-7014 as detailed above. Use of this work other than as specifically
# XXX XXX.S. XXX may violate any copyrights that exist in this work.

import matplotlib as mpl
import matplotlib.cm as cm
import cv2
from skimage.transform import resize
from transformers import AutoImageProcessor, AutoModelForDepthEstimation
from PIL import Image
import torch
import numpy as np

class Detector () :
    def __init__(self) -> None:
        checkpoint = "vinvino02/glpn-nyu"
        self.imageProcessor = AutoImageProcessor.from_pretrained(checkpoint)
        self.model = AutoModelForDepthEstimation.from_pretrained(checkpoint)

    # just for showing the matrix as an image
    def makeImage(self, input) :
        disp_resized_np = input
        vmax = np.percentile(disp_resized_np, 95)
        normalizer = mpl.colors.Normalize(vmin=disp_resized_np.min(), vmax=vmax)
        mapper = cm.ScalarMappable(norm=normalizer, cmap='magma')
        colormapped_im = (mapper.to_rgba(disp_resized_np)[:, :, :3] * 255).astype(np.uint8)
        im = Image.fromarray(colormapped_im)
        opencvImage = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        cv2.imwrite("DepthPrediction/output.jpg", opencvImage)

    def optimizeMatrix(self, matrix) :
        #number relates to size of resulting matrix.
        #resulting matrix should be around the given value squared and multiplied by 4
        SCALING_NUMBER = 50
        return self.compress_matrix(matrix, SCALING_NUMBER)
    
    def compress_matrix(self, matrix, scalingFactor):
        # Calculate the ratio of the current size to the final size
        ratio = (matrix.shape[0] * matrix.shape[1]) ** 0.5 / scalingFactor
        # Calculate the new dimensions
        new_dims = (int(matrix.shape[0] / ratio), int(matrix.shape[1] / ratio))
        # Resize the matrix
        compressed_matrix = resize(matrix, new_dims, mode='reflect', anti_aliasing=True)
        # Change data type to float16
        compressed_matrix = compressed_matrix.astype(np.float16)
        return compressed_matrix
    
    def predictImage(self, inputMedia) :
        image = opencvToPil(inputMedia)
        pixelValues = self.imageProcessor(image, return_tensors="pt").pixel_values

        with torch.no_grad():
            outputs = self.model(pixelValues)
            predictedDepth = outputs.predicted_depth

        # interpolate to original size
        prediction = torch.nn.functional.interpolate(
            predictedDepth.unsqueeze(1),
            size=image.size[::-1],
            mode="bicubic",
            align_corners=False,
        ).squeeze()
        output = prediction.numpy()
        return self.optimizeMatrix(output)
    
def opencvToPil(opencvImage):
    # Convert the color from BGR to RGB
    rgbImage = cv2.cvtColor(opencvImage, cv2.COLOR_BGR2RGB)
    # Convert to a PIL Image
    pilImage = Image.fromarray(rgbImage)
    return pilImage
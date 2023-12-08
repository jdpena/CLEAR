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

from DepthPrediction.DepthPredict import Detector
from DepthPrediction.OutputDepth import OutputDepth
import requests
import numpy as np
from PIL import Image
from skimage.transform import resize

class DepthWork() :
    GOOD_CODE = 200
    def setUp(self) :
        self.Detector = Detector()
        self.getURL = '{}/depthImage'.format(self.apiURL)
        self.postURL = '{}/depth'.format(self.apiURL)
        self.identity = "depth_perception"
        self.session = requests.Session()
        
    def getDepth(self, media) :
        self.depthnp = self.Detector.predictImage(media)

    def runWorker(self) :
        self.ready = False
        response = self.session.get(self.getURL)

        # error getting response
        if not response.status_code == self.GOOD_CODE: return
        
        self.getDepth(self.transmuteToImage(response))
        output = OutputDepth(self.depthnp).getOutput()

        response = self.session.post(self.postURL, json={'matrix': output.tolist()})
                    
        print(response.status_code)
        self.ready = True

    # just for debugging
    def testing(self) :
        media = Image.open("testingImage/catTest.jpg")

        originalDim = (media.height, media.width)
        
        self.getDepth(np.array(media))
        output = OutputDepth(self.depthnp).getOutput()

        print (output.shape[0] * output.shape[1] * 4)

        np.savetxt("DepthPrediction//testingOutputs//depthArray.txt", output)

        # Enlarge the matrix back to its original size
        matrix = output.astype(np.float32)

        decompressed_matrix = resize(matrix, originalDim, mode='reflect', anti_aliasing=True)

        self.Detector.makeImage(decompressed_matrix)


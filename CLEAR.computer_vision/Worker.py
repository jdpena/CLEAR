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

import cv2, importlib.util
import numpy as np

def makeWorker(wtype, url):
    return MyWorker(wtype)(url)

#there's an object detection model, 
#and a depth perception model
def returnWorkerType(key):
    module_name = None
    class_name = None

    if key == "obj":
        module_name = "ObjectDetection.DetectiveWork"
        class_name = "DetectiveWork"
    elif key == "dep":
        module_name = "DepthPrediction.DepthWork"
        class_name = "DepthWork"
    else:
        print(key)
        assert(True)

    module = importlib.import_module(module_name)
    return getattr(module, class_name)

def MyWorker(wtype) :
    class Worker(returnWorkerType(wtype)) :
        def __init__(self, url) -> None:
            self.apiURL = url
            self.ready = True
            self.setUp() 

        # making understandable image from web request
        def transmuteToImage(self, response) :
            img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            return img
    return Worker

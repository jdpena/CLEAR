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

from ObjectDetection.Detector import Detector
from ObjectDetection.support.OutputObj import Output
import requests
from PIL import Image
import cv2

class DetectiveWork() :
    GOOD_CODE = 200
    def setUp(self) :
        self.Detector = Detector()
        self.getURL = '{}/objectImage'.format(self.apiURL)
        self.postURL = '{}/contextInfo'.format(self.apiURL)

        self.identity = "object_detection"
        
        self.session = requests.Session()

    def getObjects(self, threshold, media) :
        self.objects = self.Detector.predictImage(media = media, 
        threshold = threshold)
    
    def runWorker(self) :
        self.ready = False
        response = self.session.get(self.getURL)
        threshold = .5

        # error getting response
        print(response)
        if not response.status_code == self.GOOD_CODE: return
        
        print ("Caught")
    
        self.getObjects(threshold, self.transmuteToImage(response))
        output = Output(self.objects)
        
        if hasattr(output, "objects" ):
            outputString = output.getOutputString()
            response = self.session.post(self.postURL, json={'string': outputString})
            print(response.status_code)
        
        self.ready = True
    
    def testing(self) :
        media = cv2.imread("ObjectDetection/images/catTest.jpg")
        media = cv2.cvtColor(media, cv2.COLOR_RGB2BGR)


        self.getObjects(0.5, media)
        output = Output(self.objects)

        if hasattr(output, "objects" ):
            outputString = output.getOutputString()
            print(outputString)


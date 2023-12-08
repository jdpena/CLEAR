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

import cv2, time
import warnings
from ultralytics import YOLO
warnings.filterwarnings('ignore')   # Suppress Matplotlib warnings
from ObjectDetection.support.DetectedItem import *
 

class SubClassDetector :
      def __init__(self, name) -> None:
            print('Loading model...', end='')
            start_time = time.time()
            self.detectFn = YOLO("{}.pt".format(name))
            end_time = time.time()
            elapsed_time = end_time - start_time
            print('Done! Took {} seconds'.format(elapsed_time))

      def specify(self, image, startX, startY) :

            print("sub start")
            results = self.detectFn.predict(source=image, conf=0.50, )  # save plotted images
            print ("sub end")
            names = self.detectFn.names

            #Element zero is the highest scoring confidence in scan.
            # return image_with_detections

            if len(results[0].boxes) :
                  objDet = results[0].boxes[0]
                  self.item = (DetectedItem(objDet.xyxy[0], 
                        names[int(objDet.cls)],
                        objDet.conf[0], image, startX, startY))
            else : 
                  self.item = None


# DISTRIBUTION STATEMENT A. Approved for public release. Distribution is unlimited.

# This material is based upon work supported by the Under Secretary of Defense for 
# Research and Engineering under Air Force Contract No. FA8702-15-D-0001. Any opinions,
# findings, conclusions or recommendations expressed in this material are those 
# of the author(s) and do not necessarily reflect the views of the Under 
# Secretary of Defense for Research and Engineering.

# © 2023 Massachusetts Institute of Technology.

# Subject to FAR52.227-11 Patent Rights - Ownership by the contractor (May 2014)

# The software/firmware is provided to you on an As-Is basis

# Delivered to the U.S. Government with Unlimited Rights, as defined in DFARS Part 
# 252.227-7013 or 7014 (Feb 2014). Notwithstanding any copyright notice, 
# U.S. Government rights in this work are defined by DFARS 252.227-7013 or 
# DFARS 252.227-7014 as detailed above. Use of this work other than as specifically
# authorized by the U.S. Government may violate any copyrights that exist in this work.

import copy, cv2, time
import numpy as np
import PIL.Image as pil
import matplotlib as mpl
import matplotlib.cm as cm

class UserInterface() :
    def __init__(self, drone) :
        self.drone = drone
        self.target = drone.intelligence.target
        # self.target = None
        self.runInterface()

    def runInterface(self) :
        # try :
        print("interface started")
        while self.drone.intelligence.droneIsRunning: 
            targ = copy.deepcopy(self.target)
            self.displayDroneView(targ)

            if self.drone.intelligence.depth.ready:
                self.displayDepthPerception()
            
            if hasattr(self.drone.intelligence, "message") :
                # self.audioOutput(self.drone.intelligence.message)
                del self.drone.intelligence.message

            time.sleep(0.25)
        exit()
        # except Exception as e: 
        #     print("interface error : {}".format(e))
        #     self.drone.intelligence.running = False

     #handles image display
    def displayDroneView(self, targ) :
        if targ.active :
            cv2.circle(self.drone.picFrame, targ.midpoint, 20, (255, 0, 0), 2)
        win = cv2.imshow("Drone",  self.drone.picFrame)
        cv2.waitKey(1) & 0xff

    # def audioOutput(self, message) :
    #     self.speechEngine.say(message)
    #     self.speechEngine.runAndWait()

    def displayDepthPerception(self) :
        disp_resized_np = copy.deepcopy(self.drone.intelligence.depth.getMatrix())
        vmax = np.percentile(disp_resized_np, 95)
        normalizer = mpl.colors.Normalize(vmin=disp_resized_np.min(), vmax=vmax)
        mapper = cm.ScalarMappable(norm=normalizer, cmap='magma')
        colormapped_im = (mapper.to_rgba(disp_resized_np)[:, :, :3] * 255).astype(np.uint8)
        im = pil.fromarray(colormapped_im)
        opencvImage = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        cv2.imshow("depth prediction", opencvImage)
        cv2.waitKey(1) & 0xff
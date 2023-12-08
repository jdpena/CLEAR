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
        while self.drone.drone.droneIsRunning: 
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
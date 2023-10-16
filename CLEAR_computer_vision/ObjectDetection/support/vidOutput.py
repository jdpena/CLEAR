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

from moviepy.editor import *
from pathlib import Path
import cv2
import numpy as np
  

# since moviepy.editor using RGB channels, while 
# openCV uses BGR, we need to need to shift things
def shiftChannels(images) :
    for i in range(len(images)) :
        images[i] = cv2.cvtColor(images[i],cv2.COLOR_BGR2RGB)
    return images

def makeVideo(images):

    images = shiftChannels(images)
    img_clips = []

    fps = 24

    for i in images :
        slide = ImageClip(i,duration=1/fps)
        img_clips.append(slide)

    #concatenating slides
    video_slides = concatenate_videoclips(img_clips, method='compose', )
    #exporting final video
    video_slides.write_videofile("output_video.mp4", fps)

def makeMedia(media) :
    if type(media) == "List" :
        makeVideo(media)
        return
    cv2.imwrite("output/" + "output" + ".jpg", media)
    cv2.imshow("Result", media)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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


"""
gmig4jowvyji
This class handles the retrieval and manipulation of images.
Using spot's two front cameras, an abstracted image is created.
""" 
import numpy as np
import cv2
from bosdyn.client.async_tasks import AsyncGRPCTask
from bosdyn.api import image_pb2
from bosdyn.client.image import ImageClient, build_image_request
from SpotController.CameraHandler.renderingImage.stitch_front_images import startRenderer


class AsyncImageCapture(AsyncGRPCTask):
    """Grab camera images from the robot."""

    def __init__(self, handler, robot, controller):
        super(AsyncImageCapture, self).__init__()
        self.handler = handler

        self.image_service = ImageClient.default_service_name
        self._image_client = (robot.ensure_client(self.image_service))
        self._video_mode = True
        self._should_take_image = False
        self.controller = controller
        self.image_sources = ["frontleft_fisheye_image", "frontright_fisheye_image"]
        self.pixel_format = "PIXEL_FORMAT_RGB_U8"

        # self.hand_source = ["hand_color_image"]
# 
        self.RENDERING = True
        if self.RENDERING:
            self.renderer = startRenderer(self._image_client)
        
        #determines how much overlap exists for width of images
        self.controller.imageOverlap = 0.05

        self.imgFlip = 0

    def toggle_video_mode(self):
        """Toggle whether doing continuous image capture."""
        self._video_mode = not self._video_modef

    def take_image(self):
        """Request a one-shot image."""
        self._should_take_image = True

    def _start_query(self):
        self._should_take_image = False

        return self.get_images_from_robot()

    def _should_query(self, now_sec):  # pylint: disable=unused-argument
        return self._video_mode or self._should_take_image

    #Removes 5% of image and then stitches the two images together.
    #Additionally, the stiched piece is then blurred to make the transition easier
    def blend_and_save_images(self, images):
        images.reverse()
        overlap = int(images[0].shape[1] * self.controller.imageOverlap)
        images[0] = images[0][:, :images[0].shape[1]-overlap]
        images[1] = images[1][:, overlap:]

        for i in range(overlap * 2):
            alpha = i / (overlap * 2)
            beta = 1.0 - alpha
            images[0][:, -i] = alpha * images[0][:, -i] + beta * images[1][:, i]

        combined_image = np.hstack(images)
        self.controller.image = combined_image
        self.controller.grabimage = combined_image

    def process_images(self, image_responses):
        images = []
        self.controller.showImages = []

        for image in image_responses:
            num_bytes = 3
            dtype = np.uint8

            img = np.frombuffer(image.shot.image.data, dtype=dtype)
            if image.shot.image.format == image_pb2.Image.FORMAT_RAW:
                try:
                    img = img.reshape((image.shot.image.rows, image.shot.image.cols, num_bytes))
                except ValueError:
                    img = cv2.imdecode(img, -1)
            else:
                img = cv2.imdecode(img, -1)

            self.controller.showImages.append(img.copy())
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            images.append(img)

        self.controller.images = image_responses
        return images

    def _handle_result(self, result):        
        if hasattr(self.handler, "arm") and self.handler.arm.readyToGrab:
            images = self.process_images(result)
            self.blend_and_save_images(images)
        else:
            self.controller.image = self.renderer.getImage()

    def _handle_error(self, exception):
        LOGGER.exception('Failure getting image: %s', exception)
    
    def get_images_from_robot(self):
        # Capture images
        pixel_format_enum = self.pixel_format_string_to_enum(self.pixel_format)
        image_request = [
            build_image_request(source, pixel_format=pixel_format_enum)
            for source in self.image_sources
        ]
        image_responses = self._image_client.get_image_async(image_request)

        return image_responses
    

    def pixel_format_string_to_enum(self, enum_string):
        return dict(image_pb2.Image.PixelFormat.items()).get(enum_string)

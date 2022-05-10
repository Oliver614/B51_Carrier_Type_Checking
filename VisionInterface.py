"""
VisionInterface.py
Oliver Hodgson 04/05/2022

Contains functions needed to use the Flir Blackfly S USB-3 Cameras used in this project.

Since 2 cameras are being used for increased accuracy two cameras need to be setup.
Image Acquisition then happens firstly iterating over the images to be taken and then
returning them to be evaluated by the neural net.
"""

from io import BytesIO
from Log import Logger
from PIL import Image
import PySpin   # Flir library for accessing cameras using python


def merge_images(file1, file2):
    """
    Merge two images into one, displayed side by side
    :param file1: path to first image file
    :param file2: path to second image file
    :return: the merged Image object
    """
    image1 = Image.open(file1)
    image2 = Image.open(file2)

    (width1, height1) = image1.size
    (width2, height2) = image2.size

    result_width = width1 + width2
    result_height = max(height1, height2)

    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(width1, 0))
    return result


class VisionInterface:
    """
    Encapsulation of the cameras and their functions.
    """
    def __init__(self):
        self.name = 'Cameras'
        self._instance = PySpin.System.GetInstance()
        self._cam_list = []
        self._cam_serial_numbers = []
        self._NUM_EXPECTED_CAMERAS = 2
        self._NUM_IMAGES = 1
        self._num_cameras = 0
        # version = self._instance.GetLibraryVersion()
        # TODO: Log version found.

    def __del__(self):
        # Clear camera list before releasing system
        self._cam_list.clear()
        # Release system instance
        self._instance.ReleaseInstance()

    def get_camera_list(self):
        return self._cam_list

    def init_cameras(self):
        """
        Initialises cameras for use.
        :return: false if less than _NUM_EXPECTED_CAMERAS amount of cameras is found.
        """
        self._cam_list = self._instance.GetCameras()
        self._num_cameras = self._cam_list.GetLength()

        if self._num_cameras < self._NUM_EXPECTED_CAMERAS:
            Logger.log_error(self.name, 'Not enough cameras found, Check camera connections.')
            return False

        for i, cam in enumerate(self._cam_list):
            node_device_serial_number = PySpin.CStringPtr(cam.GetTLDeviceNodeMap().GetNode('DeviceSerialNumber'))
            Logger.log_info(self.name, "Camera {} Found: {}".format(i, node_device_serial_number))
            self._cam_serial_numbers.append(node_device_serial_number)

        return True

    def take_images(self):
        """
        Accesses the camera and returns a list of images.
        Save the images if save_images is true.
        :return: Merges PIL.jpeg images if successful, false if not.
        """
        a = BytesIO()
        b = BytesIO()
        images_list = [a, b]
        try:
            for cam in self._cam_list:
                cam.Init()

            for n in range(self._NUM_IMAGES):
                for i, cam in enumerate(self._cam_list):

                    # Get the Image
                    cam.BeginAcquisition()
                    image_result = cam.GetNextImage()

                    # Check if the image was taken successfully
                    if image_result.IsIncomplete():
                        Logger.log_error(self.name, 'Image incomplete with image status %d'
                                         % image_result.GetImageStatus())
                        return False

                    # Save as a temp image, this will be overwritten every new image taken
                    image_to_save = image_result.Convert(PySpin.PixelFormat_RGB8, PySpin.HQ_LINEAR)

                    image_to_save.Save(images_list[i], format='jpeg')
                    image_result.Release()

            for cam in self._cam_list:
                cam.DeInit()
                cam.EndAcquisition()

            return merge_images(images_list[0], images_list[1])

        except PySpin.SpinnakerException as ex:
            Logger.log_error(self.name, 'Error: %s' % ex)
            return False

# end of camera class

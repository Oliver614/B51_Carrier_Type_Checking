"""
Contains some general purpose functions that don't need to belong
to any particular object
"""

from tkinter import filedialog
from datetime import datetime
from io import BytesIO
from PIL import Image


def merge_images(file1, file2):
    """Merge two images into one, displayed side by side
    :param file1: path to first image file
    :param file2: path to second image file
    :return: the merged Image object
    """
    image1 = Image.open(file1)
    image2 = Image.open(file2)

    print(type(image1))

    (width1, height1) = image1.size
    (width2, height2) = image2.size

    result_width = width1 + width2
    result_height = max(height1, height2)

    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(width1, 0))

    b = BytesIO()
    result.save(b, format='jpeg')

    return Image.open(b)


def resize_image(image: Image):
    (width, height) = image.size
    aspect_ratio = width / height
    new_height = 400
    new_width = int(new_height * aspect_ratio)
    new_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    return new_image


def save_image(image, carrier_type="", manual_save=False):
    """
    Saves an image to the specified folder, gives it a name automatically
    :param image: The image to save
    :param carrier_type: The carrier type for the folder to put it in when it saves automatically
    :param manual_save: True when using the GUI button false for if done by the program
    :return: none
    """
    if manual_save:
        directory = filedialog.askdirectory(initialdir="/Images/")
        save_to = directory + '/' + datetime.now().strftime("%Y%m%d%H%M%S") + '.jpg'
        image.save(save_to)
    else:
        location = "Images/{}/{}.jpg".format(carrier_type,datetime.now().strftime("%Y%m%d%H%M%S"))
        image.save(location)
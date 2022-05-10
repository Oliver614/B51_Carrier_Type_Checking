"""

Contains classes for creating pre-trained neural net for classification of the carriers.

"""

from enum import Enum
from tensorflow.python.keras import models
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

MODEL_LOCATION = ''


class NeuralNet:
    """

    """
    MODEL = models.load_model(MODEL_LOCATION)

    @staticmethod
    def classify(image):
        """
        Classifies the new images taken with the pre-trained model.
        :param image: Image Data from the cameras
        :return: List [Type, Probability]
        """
        img = image.load_img(image, target_size=(150, 150))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        images = np.vstack([x])
        classes = NeuralNet.MODEL.predict(images, batch_size=10)

        return classes


class NewModel:
    """
    Class used for training new neural networks if it ever comes to it.
    """
    def __init__(self):
        self.name = 'NewModel'
        self.model = None

    def get_data(self, filepath):
        """
        Gets new images from the specified filepath,
        :param filepath: where the images are stored
        :return: image data ready for training
        """
        data = False

        train_datagen = ImageDataGenerator(rescale=1./255, rotation_range=10)
        val_datagen = ImageDataGenerator(rescale=1./255)
        test_datagen = ImageDataGenerator(rescale=1./255)

        # Get the Images from the specified filepath.
        train_data = train_datagen.flow_from_directory('{}/train/'.format(filepath), class_mode='categorical')
        validation_data = val_datagen.flow_from_directory('{}/validation/'.format(filepath), class_mode='categorical')
        test_data = test_datagen.flow_from_directory('{}/test/'.format(filepath), class_mode='categorical')

        return train_data, validation_data, test_data

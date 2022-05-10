
from PIL import Image, ImageFilter, ImageEnhance

image_kernel_5X5 = (-1, -1,  1.8, -1, -1,
                    -1, -1,  1.8, -1, -1,
                    0.1,  0.1,   11,  0.1,  0.1,
                    -1, -1,  1.8, -1, -1,
                    -1, -1,  1.8, -1, -1,)


def to_monochrome(image: Image):
    """
    Turns a colour image in B&W
    :param image: the image to convert
    :return: the new B&W Image
    """
    return image.convert("L")


def process_image(image: Image, kernel=image_kernel_5X5, contrast_amount: float = 1):
    """
    Process an image for the Neural Network, this makes it easier to find features.
    :param image: The image to enhance
    :param kernel: The kernel used for the convolution 5x5 matrix needed. Leave blank if using default
    :param contrast_amount: the amount of contrast wanted. Leave blank for no contrast
    :return: the processed image
    """
    image_ = image
    image_ = to_monochrome(image_)
    image_ = image_.filter(ImageFilter.Kernel((5, 5), kernel, 1, 0))
    image_enhancer = ImageEnhance.Contrast(image_)
    image_enhanced_ = image_enhancer.enhance(contrast_amount)
    return image_enhanced_


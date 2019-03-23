import os
import re
from werkzeug.datastructures import FileStorage
from resizeimage import resizeimage
from flask_uploads import UploadSet, IMAGES
from PIL import Image

IMAGE_SET = UploadSet("images", IMAGES)  # set name and allowed extensions


def save_image(image: FileStorage, folder: str = None, name: str = None):
    """Takes FileStorage and saves it to a folder"""
    return IMAGE_SET.save(image, folder, name)


def get_path(filename: str = None, folder: str = None):
    """Take image name and folder and return full path"""
    return IMAGE_SET.path(filename, folder)


def find_image_any_format(filename: str, folder: str):
    """Takes a filename and returns an image on any of the accepted formats."""
    for _format in IMAGES:
        image = f"{filename}.{_format}"
        image_path = IMAGE_SET.path(filename=image, folder=folder)
        if os.path.isfile(image_path):
            return image_path
    return None


def _retrieve_filename(file):
    """Take FileStorage and return the filename"""
    if isinstance(file, FileStorage):
        return file.filename
    return file


def is_filename_safe(file):
    """Check regex and return whether the string matches or not"""
    filename = _retrieve_filename(file)
    allowed_format = "|".join(IMAGES)  # png|svg|jpe|jpg|jpeg
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def get_basename(file):
    """Return full name of image in the path"""
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]


def get_extension(file):
    """Return file extension"""
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]


def resize(path):
    with open(path, "r+b") as f:
        with Image.open(f) as image:
            img = image
            if image.width >= 300:
                img = resizeimage.resize_width(image, 300)
            img.save(path, image.format)

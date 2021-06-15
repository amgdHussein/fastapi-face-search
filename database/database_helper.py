import os
from io import BytesIO

import face_recognition
from fastapi.datastructures import UploadFile
from numpy import asarray
from PIL import ExifTags, Image


def is_allowed_extension(name: str) -> bool:
    return os.path.splitext(name.lower())[1] in ('.jpg', '.jpeg', '.png')


def has_face(image: Image.Image) -> bool:
    image_encoding = face_recognition.face_encodings(asarray(image))

    # check if there is any face exists in the image
    if len(image_encoding) == 0:
        return False

    return True


async def read_image_file(file: UploadFile) -> Image.Image:
    # check if file is an image with jpg, jpeg, png
    if is_allowed_extension(name=file.filename):
        myfile = await file.read()
        image_file = BytesIO(myfile)
        image = fix_orientation(image=Image.open(image_file))
        image.filename = file.filename

        # check if there is any face exists in the image
        if has_face(image=image):
            return image

        raise Exception('No face detected!')

    raise Exception('Image must be jpg, jpeg or png format!')


def fix_orientation(image: Image.Image) -> Image.Image:
    THUMB_WIDTH, THUMB_HIGHT = 1000, 1000
    if hasattr(image, '_getexif'):
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        e = image._getexif()
        if e is not None:
            exif = dict(e.items())
            orientation = exif[orientation]

            if orientation == 3:
                image = image.transpose(Image.ROTATE_180)
            elif orientation == 6:
                image = image.transpose(Image.ROTATE_270)
            elif orientation == 8:
                image = image.transpose(Image.ROTATE_90)

        image.thumbnail((THUMB_WIDTH, THUMB_HIGHT), Image.ANTIALIAS)

    return image

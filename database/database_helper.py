import face_recognition
from fastapi import UploadFile, File
from numpy import asarray
from PIL import Image
from io import BytesIO


def check_extension(file: UploadFile):
    extension = file.filename.split('.')[-1].lower() in ('jpg', 'jpeg', 'png')
    if not extension:
        return 'Image must be jpg or png format!'


def has_face(image: Image.Image) -> bool:
    image_encoding = face_recognition.face_encodings(asarray(image))

    # check if there is any face exists in the image
    if len(image_encoding) == 0:
        return False

    return True


async def read_image_file(file: File):
    myfile = await file.read()
    image_file = BytesIO(myfile)
    image = Image.open(image_file)
    if has_face(image=image):
        # check if there is any face exists in the image
        return image

    raise Exception('No face detected.')

from os import listdir, remove
from os.path import exists, join, splitext
import glob

from __init__ import DEFAULT_DIR, HOST, PORT
from PIL import Image


# Image File Description
#   > image_name = 9898n393k.jpg
#       - post_id = 9898n393k


async def read_images() -> list:
    images = []
    for image_name in listdir(DEFAULT_DIR):
        known_person = await read_image(file_name=image_name)
        images.append(known_person)

    return images


async def read_image(file_name: str) -> Image.Image:
    image_path = await retrieve_image(file_name=file_name)
    if image_path:
        return Image.open(image_path)


async def add_image_file(image: Image.Image, pid: str) -> str:
    file_name = pid + splitext(image.filename)[1]
    dir = join(DEFAULT_DIR, file_name)
    image.save(dir)

    return f'http://{HOST}:{PORT}/api/filesys/retrieve/image/{pid}'


async def retrieve_image(file_name: str) -> str:
    dir = join(DEFAULT_DIR, file_name)
    file_dir = glob.glob(dir + '.*')
    if len(file_dir) > 0:
        return file_dir[0]


async def delete_image_file(file_name: str) -> bool:
    dir = join(DEFAULT_DIR, file_name)
    file_dir = glob.glob(dir + '.*')

    if file_dir:
        remove(path=file_dir[0])
        return True

    return False

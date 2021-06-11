import os
from fastapi import File
from PIL import Image
from .database_helper import read_image_file

# Image File Description
#   > image_name = **Majda El-Roumi.9898n393k.jpg**
#       - person_name = Majda El-Roumi
#       - image_id = 9898n393k
#       - image_extension = jpg

DEFAULT_DIR = os.path.join('database', 'images')


async def retrieve_images() -> list:
    images = []
    for image_name in os.listdir(DEFAULT_DIR):
        known_person = await retrieve_image(file_name=image_name)
        images.append(known_person)
        # yield known_person, image_name
    return images


async def add_image_file(file: File) -> Image.Image:
    image = await read_image_file(file=file)
    if image:
        image.save(os.path.join(DEFAULT_DIR, file.filename))
        return file.filename

    raise Exception('The face cannot be recognized.')


async def retrieve_image(file_name: str) -> Image.Image:
    dir = os.path.join(DEFAULT_DIR, file_name)
    if os.path.exists(dir):
        return Image.open(dir)


async def delete_image_file(file_name: str) -> bool:
    dir = os.path.join(DEFAULT_DIR, file_name)
    if os.path.exists(dir):
        os.remove(path=dir)
        return True
    return False

# async def update_post_data(id: str, data: dict):
#     post = await post_collection.find_one({'_id': ObjectId(id)})
#     if post:
#         post_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
#         return True

# async def update_image(file: UploadFile = File(...)):
#     image_dir = os.path.join(DEFAULT_DIR, file.filename)
#     if os.path.exists(path=image_dir):
#         os.remove(path=image_dir)
#     else:
#         raise HTTPException(
#             status_code=404,
#             detail='Image file not found.',
#         )

    # check_extension(file=file)

    # imagefile = await file.read()
    # image = read_imagefile(file=imagefile)

    # image.save(os.path.join(DEFAULT_DIR, file.filename))

    # return {
    #     'updated': True
    # }

from fastapi import APIRouter
from database.database import *
from models.post_image_model import *
from fastapi import File, UploadFile
from face_search.face_recognition import fetch_person

router = APIRouter()


@router.get('/database/retrieve/images/', response_description='Images retrieved')
async def get_images():
    images = await retrieve_images()
    if len(images) > 0:
        return ResponseModel(
            data={
                image.filename.split('.')[1]: image.filename.split('.')[0] for image in images
            },
            message='Images data retrieved successfully',
        )

    return ErrorResponseModel(
        error='An error occured.',
        code=404,
        message='Database is empty.',
    )


@router.get('/database/retrieve/image/{id}', response_description='Image data retrieved')
async def get_image(id: str):
    image = await retrieve_image(file_name=id)
    if image:
        return ResponseModel(
            data=image.filename,
            message='Image data retrieved successfully',
        )

    return ErrorResponseModel(
        error='An error occured.',
        code=404,
        message='Image doesn\'t exist.',
    )


@router.post('/database/add/image/', response_description='Image data added')
async def add_image(image: UploadFile = File(...)):
    try:
        id = await add_image_file(file=image)

    except Exception as error:
        return ErrorResponseModel(
            error='An error occured.',
            code=422,
            message=error.args[0],
        )

    return ResponseModel(
        data=id,
        message='Image added successfully.',
    )


@router.delete('/database/delete/image/{id}', response_description='Image data deleted')
async def delete_image(id: str):
    deleted_image = await delete_image_file(file_name=id)
    if deleted_image:
        return ResponseModel(
            data='Image with ID: {} removed'.format(id),
            message='Image deleted successfully',
        )

    return ErrorResponseModel(
        error='An error occured',
        code=404,
        message='Image with id {} doesn\'t exist'.format(id),
    )


# @router.put('{id}')
# async def update_image(id: str, req: UpdateImageModel = Body(...)):
#     updated_image = await update_image_data(id, req.dict())

#     if updated_image:
#         return ResponseModel(
#             data='Image with ID: {} name update is successful'.format(id),
#             message='Image name updated successfully',
#         )

#     return ErrorResponseModel(
#         error='An error occurred',
#         code=404,
#         message='There was an error updating the image with id {}.'.format(id),
#     )


@router.post('/recognize/image/')
async def recognize_image(file: UploadFile = File(...)):
    try:
        image = await read_image_file(file=file)
    except Exception as error:
        return ErrorResponseModel(
            error='An error occured.',
            code=422,
            message=error.args[0],
        )

    predictions = await fetch_person(image=image)
    return ResponseModel(
        data={path: diff for diff, path in predictions},
        message='Image recognized successfully',
    )

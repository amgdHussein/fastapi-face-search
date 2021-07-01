from database.database import *
from database.database_helper import read_image_file
from face_search.face_recognition import fetch_person
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from models.responses import *

router = APIRouter()


@router.get('/filesys/retrieve/image/{pid}', response_description='Image retrieved')
async def get_image(pid: str):
    image_path = await retrieve_image(file_name=pid)
    if image_path:
        return FileResponse(path=image_path)

    return ErrorResponseModel(
        error='An error occured.',
        code=404,
        message='Image doesn\'t exist.',
    )


@router.post('/filesys/add/image/', response_description='Image added')
async def add_image(pid: str, file: UploadFile = File(...)):
    try:
        image = await read_image_file(file=file)
        link = await add_image_file(image=image, pid=pid)
        return ResponseAddModel(
            download_link=link,
            message='Image added successfully.',
        )

    except Exception as error:
        return ErrorResponseModel(
            error='An error occured.',
            code=422,
            message=error.args[0],
        )


@router.delete('/filesys/delete/image/{pid}', response_description='Image deleted')
async def delete_image(pid: str):
    isdeleted = await delete_image_file(file_name=pid)
    if isdeleted:
        return ResponseDeleteModel(
            data='Image with pid: {} removed'.format(pid),
            message='Image deleted successfully',
        )

    return ErrorResponseModel(
        error='An error occured',
        code=404,
        message='Image with pid {} doesn\'t exist'.format(pid),
    )


@router.post('/recognize/image/', response_description='Image recognized')
async def recognize_image(file: UploadFile = File(...)):
    try:
        image = await read_image_file(file=file)
        predictions = await fetch_person(image=image)
        return ResponseRecognitionModel(
            ids=[id for id, diff in predictions],
            message='Image recognized successfully',
        )

    except Exception as error:
        return ErrorResponseModel(
            error='An error occured.',
            code=422,
            message=error.args[0],
        )


@router.post('/recognize/is_valid/image/', response_description='Image validation')
async def add_image(file: UploadFile = File(...)):
    try:
        image = await read_image_file(file=file)
        return ResponseValidatedImage(is_valid=True)

    except Exception as error:
        return ErrorResponseModel(
            error='An error occured.',
            code=422,
            message=error.args[0],
        )

from typing import Optional
from pydantic import BaseModel


# class UpdatePostModel(BaseModel):
#     post_id: str = Optional[str]

#     class Config:
#         schema_extra = {
#             "example": {
#                 "post_id": "klsdjawq89n",
#             }
#         }


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }

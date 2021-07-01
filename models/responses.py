def ResponseAddModel(download_link, message) -> dict:
    return {
        "link": download_link,
        "code": 200,
        "message": message,
    }

def ResponseDeleteModel(data, message) -> dict:
    return {
        "deleted": data,
        "code": 200,
        "message": message,
    }

def ResponseRecognitionModel(ids, message) -> dict:
    return {
        "pids": ids,
        "code": 200,
        "message": message,
    }

def ResponseValidatedImage(is_valid) -> dict:
    return {
        "valid": is_valid,
        "code": 200,
    }

def ErrorResponseModel(error, code, message) -> dict:
    return {
        "error": error,
        "code": code,
        "message": message
    }

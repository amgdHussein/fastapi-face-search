def ResponseAddModel(download_link, message):
    return {
        "link": download_link,
        "code": 200,
        "message": message,
    }

def ResponseDeleteModel(data, message):
    return {
        "deleted": data,
        "code": 200,
        "message": message,
    }

def ResponseRecognitionModel(ids, message):
    return {
        "pids": ids,
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }

import face_recognition
from numpy import array, asarray
from PIL.Image import Image
from database.database import retrieve_images


def image_to_code(image: array):
    return face_recognition.face_encodings(face_image=image)[0]


# Start engine
async def search(image: Image):
    '''
    Detector isn't able to find a face in the image:
        1. The face is turned sideways or upside-down
        2. The face is turned too sideways away from the camera instead of looking straight into the camera
        3. The face is too small in the image
    '''

    # read unknown person and encode
    unknown_image = asarray(image)

    # read all known people images
    known_people_images = await retrieve_images()
    names = list(map(lambda image: image.filename, known_people_images))
    known_people_images = list(map(asarray, known_people_images))
    # for each person fetch and encode face
    known_people_encodings = list(map(image_to_code, known_people_images))
    # encode unkown face
    unknown_image_encoding = image_to_code(unknown_image)

    # calc the code difference
    face_distances = face_recognition.face_distance(
        known_people_encodings,
        unknown_image_encoding
    )

    # compares = face_recognition.compare_faces(known_people_encodings, unknown_image_encoding[0]\]
    return names, face_distances

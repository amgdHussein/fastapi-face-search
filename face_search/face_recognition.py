from __init__ import THRESHOLD
from PIL.Image import Image

from face_search.search import search


# start search
async def fetch_person(image: Image, threshold: float = THRESHOLD):
    results = await search(image=image)
    filter_results = list(
        filter(lambda res: res[1] < threshold, list(zip(*results))))

    return filter_results

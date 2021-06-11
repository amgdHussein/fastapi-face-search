from face_search.search import search
from PIL.Image import Image


# maximum difference
THRESHOLD = 0.6

# start search


async def fetch_person(image: Image, threshold: float = THRESHOLD):
    results = await search(image=image)
    filter_results = list(
        filter(lambda res: res[1] < threshold, list(zip(*results))))

    return filter_results

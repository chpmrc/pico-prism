import requests
from io import BytesIO
from PIL import Image


def url2img(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def img2file(img):
    # TODO determine image type from image object
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=100)
    img_io.seek(0)
    return img_io


def resize(url, width, height):
    img = url2img(url)
    return img.resize((width, height))
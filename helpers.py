import requests
from io import BytesIO
from PIL import Image


def get_crop_coordinates(gravity, img, width, height):
    # Ref: https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#PIL.Image.Image.crop
    if gravity == 'center':
        return (
            img.width / 2 - width / 2,
            img.height / 2 - height / 2,
            img.width / 2 + width / 2,
            img.height / 2 + height / 2,
        )
    if gravity == 'top_left':
        return (0, 0, width, height)
    if gravity == 'top_right':
        return (img.width - width, 0, img.width, height)
    if gravity == 'bottom_right':
        return (img.width - width, img.height - height, img.width, img.height)
    if gravity == 'bottom_left':
        return (0, img.height - height, width, img.height)


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


def resize(url, width=0, height=0, crop=False, gravity='top_left'):
    img = url2img(url)
    new_height = height
    new_width = width
    only_width = bool(width and not height)
    only_height = bool(height and not width)
    neither = bool(not width and not height)
    is_portrait = img.height >= img.width
    is_landscape = not is_portrait
    if only_width or (crop and is_landscape):
        wpercent = (width/float(img.size[0]))
        height = int((float(img.size[1])*float(wpercent)))
    if only_height or (crop and is_portrait):
        hpercent = (height/float(img.size[1]))
        width = int((float(img.size[0])*float(hpercent)))
    if neither:
        width = img.width
        height = img.height
    img = img.resize((width, height), Image.ANTIALIAS)
    if crop:
        if is_portrait:
            coordinates = get_crop_coordinates(gravity, img, new_width, img.height)
        else:
            coordinates = get_crop_coordinates(gravity, img, img.width, new_height)
        img = img.crop(coordinates)
    return img

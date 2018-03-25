import logging
import traceback
from io import BytesIO, StringIO

import requests
from flask import Flask, Response, request, send_file
from PIL import Image

from helpers import img2file, resize, url2img, InvalidSize


app = Flask(__name__)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


DOCS = """
Parameters:
    - url: URL to the image to manipulate
    - op: one of [`resize`]
    - width: int (optional if height is defined)
    - height: int (optional if width is defined)
    - crop: boolean
    - gravity: only used for cropping, one of [`center`, `top_left`, `bottom_left`, `top_right`, `bottom_right`], default is `center`
"""


@app.route("/")
def main():
    try:
        url = request.args.get('url')
        op = request.args.get('op')
        width = int(request.args.get('width', 0))
        height = int(request.args.get('height', 0))
        crop = bool(request.args.get('crop', False))
        gravity = request.args.get('gravity', 'center')
        if op == 'resize':
            return send_file(img2file(resize(url, width, height, crop=crop, gravity=gravity)), mimetype='image/jpeg')
        else:
            return send_file(img2file(url2img(url)), mimetype='image/jpeg')
    except Exception:
        logger.error(traceback.format_exc())
        return Response("Something went wrong (invalid width/height?). Please read the docs below:\n{}".format(DOCS), status=400, mimetype='text/plain')


@app.route("/docs")
def docs():
    return Response(DOCS, mimetype='text/plain')

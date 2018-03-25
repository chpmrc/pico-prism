from flask import Flask, request, send_file
from io import BytesIO, StringIO
from PIL import Image
import requests
from helpers import img2file, url2img, resize
app = Flask(__name__)


@app.route("/")
def main():
    url = request.args.get('url')
    op = request.args.get('op')
    width = int(request.args.get('width', 0))
    height = int(request.args.get('height', 0))
    crop = bool(request.args.get('crop', False))
    gravity = request.args.get('gravity', 'bottom_left')
    if op == 'resize':
        return send_file(img2file(resize(url, width, height, crop=crop, gravity=gravity)), mimetype='image/jpeg')
    else:
        return send_file(img2file(url2img(url)), mimetype='image/jpeg')

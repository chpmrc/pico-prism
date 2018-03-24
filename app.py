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
    if op == 'resize':
        width = int(request.args.get('width'))
        height = int(request.args.get('height'))
        return send_file(img2file(resize(url, width, height)), mimetype='image/jpeg')
    else:
        return send_file(img2file(url2img(url)), mimetype='image/jpeg')
    
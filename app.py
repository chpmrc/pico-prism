from flask import Flask, request, send_file
from io import BytesIO, StringIO
from PIL import Image
import requests
app = Flask(__name__)

@app.route("/")
def hello():
    url = request.args.get('url')
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=10)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
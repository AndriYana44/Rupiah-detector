from sre_constants import FAILURE, SUCCESS
import cv2, re, os
import numpy as np
import math
from PIL import Image
from matplotlib import pyplot as plt
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from OCR import get_contain
from OCR import text_to_nominal
from uang_matching import template_matching as tm

app = Flask(__name__)
Bootstrap(app)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = 'secket_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# configuration file extension 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html", nominal = None)

@app.route("/", methods=['POST'])
def upload():
    # validation if image request is null
    if 'file' not in request.files:
        flash('No file uploaded!', 400)
        return redirect(request.url)
    file = request.files['file']
    # validation if filename is null
    if file.filename == '':
        flash('No file selected!')
        return redirect(request.url)
    # validation file extension
    if file and allowed_file(file.filename):
        filename, file_extension = os.path.splitext(file.filename)
        filename = secure_filename('object.jpeg')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        file_path = './static/uploads/' + filename

        # validation height image
        picture = cv2.imread(file_path)
        h, w, c = picture.shape
        if h > 4000 and h < 4600:
            crop = picture[math.ceil((h/5)*2):math.ceil((h/3)*2), 0:w]
            cv2.imwrite('./static/uploads/' + filename, crop)

        # validation size for image uploaded
        picture = Image.open(file_path)
        dim = picture.size
        if dim[0] > 1024 and os.stat(file_path).st_size > 342720:
            picture_rsz = picture.resize((1024, 480))
            picture_rsz.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        print('Upload_image filename: ' + filename)
        SUCCESS = 'Image successfully uploaded and and displayed bellow'

        terhitung = get_contain(filename)        
        nominal = text_to_nominal(terhitung)
        if(terhitung == None):
            terhitung = tm()
            nominal = text_to_nominal(terhitung)

        return render_template('index.html', filename = filename, terhitung = terhitung, nominal = nominal, SUCCESS=SUCCESS)
    else:
        FAILURE = 'Allowed image types are: png, jpg, jpeg'
        return render_template('index.html', FAILURE = FAILURE)

if __name__ == "__main__":
    app.run(host='192.168.43.197', port=8080, debug=True)
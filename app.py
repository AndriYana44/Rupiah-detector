from sre_constants import FAILURE, SUCCESS
import cv2, re, os
import numpy as np
import math
from PIL import Image
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from OCR import get_contain, text_to_nominal
from color_matching import getHighPercentage

app = Flask(__name__)
Bootstrap(app)

UPLOAD_FOLDER = 'static/uploads/'
COLOR_RECOGNIZE = 'static/uploads/color-recognize/'

app.secret_key = 'secket_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COLOR_RECOGNIZE'] = COLOR_RECOGNIZE
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# configuration file extension 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image(image_path):
    image = Image.open(image_path, "r")
    width, height = image.size
    pixel_values = list(image.getdata())
    channels = 3
    pixel_values = np.array(pixel_values).reshape((width, height, channels))
    return pixel_values

def getAverage(item):
    red = 0
    green = 0
    blue = 0
    lenData = 0
    for item1 in item:
        for item2 in item1:
            red += item2[0]
            green += item2[1]
            blue += item2[2]
            lenData += 1
        lenData += 1
    return [round(red/lenData), round(green/lenData), round(blue/lenData)]

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
        SUCCESS = 'Image successfully uploaded and displayed bellow'

        
        terhitung = get_contain(filename)
        nominal = text_to_nominal(terhitung)
        if(nominal == '-1' or nominal == None or nominal == '0'):
            # resize
            basewidth = 400
            img = Image.open(file)
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            # save
            img.save(os.path.join(app.config['COLOR_RECOGNIZE'], filename))

            # read
            terhitung = getHighPercentage('./static/uploads/color-recognize/' + filename)
            nominal = text_to_nominal(terhitung)

        return render_template('index.html', filename = filename, terhitung = terhitung, nominal = nominal, SUCCESS=SUCCESS)
    else:
        FAILURE = 'Allowed image types are: png, jpg, jpeg'
        return render_template('index.html', FAILURE = FAILURE)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
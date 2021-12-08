from sre_constants import FAILURE, SUCCESS
import cv2, re, os
import numpy as np
import math
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from PIL import Image

from WordsToText import img2text as i2t

app = Flask(__name__)
Bootstrap(app)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = 'secket_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# declare variable nominal using regex
# PART
SE = r'\s(SE|\wE|S\w)'
DUA = r'\W((\s|\S)DUA|\wUA|D\wA|DU\w)\s'
LIMA = r'((\s|$).L(I(M(A|.)|.A)|.MA)|.IMA|.MA)\s'
PULUH = r'(.P(U(L(U(H|.)|.H)|.H)|..UH)|..LUH)'
RIBU = r'(R(I(B(U|.)|.U)|.BU)|.IBU)'
RATUS = r'(R(A(T(U(S|.)|.S)|.S)|.US)|.TUS)'

# configuration file extension 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def re_20000(text):
    DUA_PULUH = r'\W((\s|\S)DUA|\wUA|D\wA|DU\w)\W+(P(U(L(U(H|.)|.H)|.H)|..UH)|..LUH)'

    result = re.search(DUA + PULUH, text)
    result = result or re.search(DUA_PULUH, text)
    return result

def re_2000(text):
    pahlawan_2000 = r'.[+N]GERAN.\w.TASAR\w.'
    char_2000 = DUA + RIBU
    angka_2000 = r'\s([+2]\d[0]{2})\ss'

    result = re.search(pahlawan_2000, text)
    result = result or re.search(char_2000, text)
    result = result or re.search(angka_2000, text)
    return result

def condition(text):
    # ======= STRING ===========
    if len(text) > 30:
        if re.search(SE + RATUS, text) :
            return "Seratus Ribu Rupiah"
        elif re.search(LIMA + PULUH, text) :
            return "Lima Puluh Ribu Rupiah"
        elif re.search(DUA + PULUH, text) :
            return "Dua Puluh Ribu Rupiah"
        elif re.search(SE + PULUH, text) :
            return "Sepuluh ribu rupiah"
        elif re.search(LIMA + RIBU, text) :
            return "Lima ribu rupiah"
        elif re.search(DUA + RIBU, text) :
            return "Dua ribu rupiah" 
        elif re.search(SE + RIBU, text) :
            return "Seribu Rupiah" 
        # ======= NUMBERS ==========
        if re.search(r'\s([+1]\d[0]{4})\s', text):
            return "Seratus Ribu Rupiah"
        elif re.search(r'\s([+5]\d[0]{3})\s', text) or re.search(LIMA + PULUH, text):
            return "Lima Puluh Ribu Rupiah"
        elif re_20000(text):
            return "Dua Puluh Ribu Rupiah"
        elif re.search(r'\s([+1]\d[0]{3})\s', text):
            return "Sepuluh ribu rupiah"
        elif re.search(r'\s([+5]\d[0]{2})\s', text):
            return "Lima ribu rupiah"
        elif re_2000(text):
            return "Dua ribu rupiah" 
        elif re.search(r'\s([+1]\d[0]{2})\s', text):
            return "Seribu Rupiah" 
        # ======== NOT DETECTED =========
        else : 
            return None
    else :
        return 'yang anda masukan bukan uang'

def convert_to_2D(filename, matrix):
    file_path = 'image_converted/object.jpeg'
    image = cv2.imread('./static/uploads/' + filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sharpen_kernel = np.array(matrix)
    sharpen = cv2.filter2D(gray, -1, sharpen_kernel)

    img = Image.fromarray(sharpen)
    img.save(file_path)

    text = i2t(file_path)
    return text

def get_text_from_2D(filename):
    text = convert_to_2D(filename, [[1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    result = condition(text.upper())
    if result == None:
        text = convert_to_2D(filename, [[-1,-1,-1], [-1,8,0], [0,-1,-1]])
        result = condition(text.upper())
        if result == None:
            text = convert_to_2D(filename, [[3,0,-1], [0,7,-1], [-1,-2,-1]])
            result = condition(text.upper())

    return result

def text_to_nominal(terhitung):
    return {
        'Seratus Ribu Rupiah' : '100.000,00~',
        'Lima Puluh Ribu Rupiah' : '50.000,00~',
        'Dua Puluh Ribu Rupiah' : '20.000,00~',
        'Sepuluh ribu rupiah' : '10.000,00~',
        'Lima ribu rupiah' : '5.000,00~',
        'Dua ribu rupiah' : '2.000,00~',
        'Seribu Rupiah' : '1.000,00~',
        None : '0',
        'yang anda masukan bukan uang' : '-1'
    }[terhitung]

def convertL_img(filename):
    file_path = './convertL_image/' + filename
    img = Image.open('./static/uploads/' + filename)
    img_convert = img.convert('L')
    img_convert.save(file_path)
    text = i2t(file_path)
    terhitung = condition(text.upper())
    return terhitung

def convert1_img(filename):
    file_path = './convert1_image/' + filename
    img = Image.open('./static/uploads/' + filename)
    img_convert = img.convert('1')
    img_convert.save(file_path)
    text = i2t(file_path)
    terhitung = condition(text.upper())
    return terhitung

def resize_img(filename):
    file_path = './static/uploads/' + filename
    img = Image.open(file_path)
    img_resize = img.resize((1024, 480))
    img_resize.save(file_path)
    text = i2t(file_path)
    terhitung = condition(text.upper())
    if terhitung == None:
        terhitung = get_text_from_2D(filename)
        if terhitung == None:
            terhitung = convertL_img(filename)
            if terhitung == None:
                terhitung = convert1_img(filename)
    return terhitung

def get_contain(filename):
    text = i2t('./static/uploads/' + filename)
    terhitung = condition(text.upper())
    if terhitung == None:
        terhitung = resize_img(filename)
    return terhitung

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

        return render_template('index.html', filename = filename, terhitung = terhitung, nominal = nominal, SUCCESS=SUCCESS)
    else:
        FAILURE = 'Allowed image types are: png, jpg, jpeg'
        return render_template('index.html', FAILURE = FAILURE)

if __name__ == "__main__":
    app.run(host='192.168.43.150', port=8080, debug=True)

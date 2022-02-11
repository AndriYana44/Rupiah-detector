from sre_constants import FAILURE, SUCCESS
import cv2, re, os
import numpy as np
import math
from PIL import Image
from matplotlib import pyplot as plt

from WordsToText import img2text as i2t

# declare variable nominal using regex
# PART
SE = r'\s(SE|\wE|S\w)'
DUA = r'\W((\s|\S)DUA|\wUA|D\wA|DU\w)\s'
LIMA = r'((\s|$).L(I(M(A|.)|.A)|.MA)|.IMA|.MA)\s'
PULUH = r'(.P(U(L(U(H|.)|.H)|.H)|..UH)|..LUH)'
RIBU = r'(R(I(B(U|.)|.U)|.BU)|.IBU)'
RATUS = r'(R(A(T(U(S|.)|.S)|.S)|.US)|.TUS)'

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
        if re.search(r'\s([+1]\d[0]{4})\s', text) or re.search(SE + RATUS, text) :
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
        elif re.search(r'\s([+5]\d[0]{3})\s', text):
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
    print(terhitung)
    if terhitung == None:
        terhitung = resize_img(filename)

    print(terhitung)
    return terhitung

if __name__ == '__main__':
    get_contain()
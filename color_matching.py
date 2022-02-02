from PIL import Image
import numpy

def get_image(image_path):
    image = Image.open(image_path, "r")
    width, height = image.size
    pixel_values = list(image.getdata())
    channels = 3
    pixel_values = numpy.array(pixel_values).reshape((width, height, channels))
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

def detectedColor(rgb):

    # cek uang berdasarkan warna RGB
    if (rgb[0] - rgb[1]) < 2 and (rgb[0] - rgb[1]) > -10 and rgb[2] > 125:
        result = 'Dua ribu rupiah'
    elif (rgb[0] - rgb[1]) < 17 and (rgb[0] - rgb[1]) > 4 and rgb[2] > 100 and rgb[2] < rgb[0] and rgb[2] < rgb[1]:
        result = 'Lima ribu rupiah'
    elif (rgb[0] - rgb[1]) > 0 and (rgb[0] - rgb[1]) < 50 and (rgb[2] - rgb[1]) > 20 and rgb[2] > rgb[1] and rgb[0] > rgb[1]:
        result = 'Sepuluh ribu rupiah'
    elif ((rgb[0] - rgb[1]) < 0 and (rgb[0] - rgb[1]) > -80) and rgb[2] > 50 and rgb[2] < rgb[1]:
        result = 'Dua Puluh Ribu Rupiah'
    elif (rgb[0] - rgb[1]) < -14 and (rgb[0] - rgb[1]) > -40 and (rgb[2] - rgb[1]) < 60 and rgb[2] > 50 and rgb[2] > rgb[0] and rgb[2] > rgb[1]:
        result = 'Lima Puluh Ribu Rupiah'
    elif (rgb[0] - rgb[1]) > 17 and (rgb[0] - rgb[1]) < 63 and (rgb[2] - rgb[1]) < 7 and (rgb[2] - rgb[1]) > -10 and rgb[2] > 50 and rgb[2] < rgb[0]:
        result = 'Seratus Ribu Rupiah'
    else :
        result = 'yang anda masukan bukan uang'

    print(rgb)
    print(result)
    return (result)

if __name__ == '__main__':
    detectedColor()
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

def detectedColor(image):
    rgb = getAverage(image)

    # cek uang berdasarkan warna RGB
    if (rgb[0] - rgb[1]) < 30 and (rgb[0] - rgb[1]) > 0  and rgb[2] > 50 and rgb[2] < rgb[0] and rgb[2] < rgb[1]:
        result = 'Lima ribu rupiah'
    elif (rgb[0] - rgb[1]) < 0 and (rgb[0] - rgb[1]) > -24 and rgb[2] > 50 and rgb[2] < rgb[0] and rgb[2] < rgb[1]:
        result = 'Dua Puluh Ribu Rupiah'
    else :
        result = None
    return result
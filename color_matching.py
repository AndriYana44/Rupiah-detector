import cv2
import numpy as np

def getPixel(imgHsv, rgbLight, rgbDark):
    light = np.array(rgbLight, np.uint8)
    dark = np.array(rgbDark, np.uint8)

    mask = cv2.inRange(imgHsv, light, dark)
    result = np.round((cv2.countNonZero(mask) / (imgHsv.size / 3)) * 100, 2)

    # plt.imshow(mask, cmap='gray')
    # plt.show()

    return result

def getHighPercentage(path):
    img = cv2.imread(path)   # read images with opencv
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    dictResult = {}
    seratusRibu = []

    seratusRibu.append(getPixel(img_hsv, [0, 50, 5], [10, 200, 255]))       # Range HSV Seratus Ribu Rupiah
    seratusRibu.append(getPixel(img_hsv, [161, 20, 20], [180,255,255]))
    print(seratusRibu) 

    dictResult['Seratus Ribu Rupiah'] = max(seratusRibu) # get max value from list
    dictResult['Lima Puluh Ribu Rupiah'] = getPixel(img_hsv, [94, 50, 50], [120, 200, 255]) # Range HSV Lima Puluh Ribu Rupiah
    dictResult['Dua Puluh Ribu Rupiah'] = getPixel(img_hsv, [43, 50, 50], [86, 255, 255])  # Range HSV Dua Puluh Ribu Rupiah
    dictResult['Sepuluh ribu rupiah'] = getPixel(img_hsv, [130, 50, 50], [160, 255, 255]) # Range HSV Sepuluh Ribu Rupiah
    dictResult['Lima ribu rupiah'] = getPixel(img_hsv, [15, 50, 50], [36, 255, 255])   # Range HSV Lima Ribu Rupiah
    dictResult['Dua ribu rupiah'] = getPixel(img_hsv, [0, 0, 100], [255, 10, 255])     # Range HSV Dua Ribu Rupiah
    dictResult['Seribu Rupiah'] = getPixel(img_hsv, [70, 0, 180], [80, 50, 255])    # Range HSV Seribu Rupiah

    result = max(dictResult, key=dictResult.get)
    print(dictResult)
    return result
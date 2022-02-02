
import glob
import os
import cv2 
import numpy as np
import imutils 

def nominal_to_text(result):
    return {
        '100000' : 'Seratus Ribu Rupiah',
        '50000' : 'Lima Puluh Ribu Rupiah',
        '20000' : 'Dua Puluh Ribu Rupiah',
        '10000' : 'Sepuluh ribu rupiah',
        '5000' : 'Lima ribu rupiah',
        '2000' : 'Dua ribu rupiah',
        '1000' : 'Seribu Rupiah'
    }[result]

def template_matching():
    # load template
    list_dir = os.listdir('template')
    template_data = []
    for dir in list_dir:
        template_files = glob.glob('template/' + dir + '/*.jpg', recursive=True)
        # prepare template
        for template_file in template_files:
            tmp = cv2.imread(template_file)
            tmp = imutils.resize(tmp, width=int(tmp.shape[1]*0.5))  # scalling
            tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)  # grayscale
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            tmp = cv2.filter2D(tmp, -1, kernel) #sharpening
            tmp = cv2.blur(tmp, (3, 3))  # smoothing
            tmp = cv2.Canny(tmp, 50, 200)  # Edge with Canny 
            nominal = template_file.replace('template\\', '').replace('.jpg', '')
            template_data.append({"glob":tmp, "nominal":nominal})
            
     
    # template matching
    # for image_glob in glob.glob('test/*.jpg'):
    detected = []
    acuracy = []
    for template in template_data:
        # image_test = cv2.imread(image_glob)
        image_test = cv2.imread('./static/uploads/object.jpeg')
        # image_test = cv2.imread()
        (tmp_height, tmp_width) = template['glob'].shape[:2]

        image_test_p = cv2.cvtColor(image_test, cv2.COLOR_BGR2GRAY) 

        image_test_p = cv2.Canny(image_test_p, 50, 200)

        found = None
        thershold = 0.4
        for scale in np.linspace(0.2, 1.0, 20)[::-1]: 
            # scalling uang
            resized = imutils.resize(
                image_test_p, width=int(image_test_p.shape[1] * scale))
            r = image_test_p.shape[1] / float(resized.shape[1]) 
            if resized.shape[0] < tmp_height or resized.shape[1] < tmp_width:
                break

            # template matching
            cv_coeff = 'TM_CCOEFF_NORMED'
            match_coeff = getattr(cv2, cv_coeff)
            result = cv2.matchTemplate(resized, template['glob'], match_coeff)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
            if found is None or maxVal > found[0]:
                if maxVal >= thershold: 
                    detected.append({"acuracy":round(maxVal, 3), "nominal":template['nominal']})
                    acuracy.append(round(maxVal, 3))

            if found is not None: 
                (maxVal, maxLoc, r) = found
                (startX, startY) = (int(maxLoc[0]*r), int(maxLoc[1] * r))
                (endX, endY) = (
                    int((maxLoc[0] + tmp_width) * r), int((maxLoc[1] + tmp_height) * r))
                if maxVal >= thershold:
                    cv2.rectangle(image_test, (startX, startY), (endX, endY), (0, 0, 255), 2)
        
    hasil = None
    for res in detected:
        if max(acuracy) == res['acuracy']:
            result_nominal = res['nominal']
            result_list = result_nominal.split('/')
            result_fix = result_list[1]
            hasil = nominal_to_text(result_fix)

            print(detected)
            print(hasil)
            return hasil

if __name__ == '__main__':
    template_matching()
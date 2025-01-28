from paddleocr import PaddleOCR # library for OCR(Optical character recognition)

import logging # disable the debug msg
logging.disable(logging.DEBUG) 
logging.disable(logging.WARNING)

def OCR(img):
    '''
    return the all the texts detected in the image
    '''
    li=[]
    ocr = PaddleOCR(lang='en')
    img_path = img
    result = ocr.ocr(img_path, cls=False)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            li.append(line[-1][0].lower()) # print the text detected
    print(li)
    return li


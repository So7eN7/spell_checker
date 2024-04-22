import cv2
import pytesseract
import numpy as np

def analyze(path):
    src = cv2.imread(f'{path}')
    cv2.imshow('', src)
    output_txt = pytesseract.image_to_string(src)
    print(type(output_txt))
    print(output_txt)
    cv2.waitKey(0)
    return output_txt 

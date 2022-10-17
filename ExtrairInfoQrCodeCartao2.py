import os
import cv2
import numpy as np
import sys, qrcode
import pyqrcode
import qrtools
from pdf2image import *
sys.stdout.reconfigure(encoding='utf-8')
#from poppler import load_from_file, PageRenderer
#from popplerutils import *


# Morph close
global q

# Find contours and filter for QR code
def findContours(image, close, original):
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    
    #if(q is None):
    #    q = 0 
    
    ROI = False
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        x,y,w,h = cv2.boundingRect(approx)
        area = cv2.contourArea(c)
        ar = w / float(h)
        if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
            cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
            ROI = original[y:y+h, x:x+w]
    #q = q + 1
    s = "ROI" + ".png"
    cv2.imwrite(s ,ROI)
    return ROI

def extractValueFromQrCode(img):
    detector=cv2.QRCodeDetector()
    val,b,c=detector.detectAndDecode(img)
    return val

def main():
    directory = 'cartoesPDF'
    fi = open("QrCodesRead.txt", "w")
    n = 0
    m = 0
   # fi.write("Inicio")
    fi.close()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
    # checking if it is a file
        if os.path.isfile(f) and f.find(".pdf") > 0:
            m = m + 1
            filename = f.replace(".\\","")
            #print("Lendo arquivo: " + f)
            images = convert_from_path(f,dpi=100,fmt="ppm")
            images[0].save("a.tiff", "tiff")
            # Load imgae, grayscale, Gaussian blur, Otsu's threshold
            image = cv2.imread("a.tiff") #cv2.imread(images[0])
            original = image.copy()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (9,9), 0)
            thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
            close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
            try:
                img = findContours(image, close, original)
                qrCode = extractValueFromQrCode(img)
                #print("Qr Code: " + qrCode)
                if(qrCode != "" and qrCode is not None):
                    n= n+1
                    fi = open("QrCodesRead.txt", "a")
                    fi.write(qrCode + "\r\n");
                    fi.close()
            except:
                print("Erro no processamento do QR Code")
                continue
    print("Nro QrCode lidos: ", n, "/",m)

main()



    


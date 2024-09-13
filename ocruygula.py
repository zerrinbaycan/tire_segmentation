import cv2
import os
import easyocr
import numpy as np

#Ocr ile yazı olan bölgeleri bulmayı sağlar
def detectocrtext(image,filename,path):
    fname = os.path.join(path, 'OCR')
    if not os.path.exists(fname):
        os.mkdir(fname)

    fname = os.path.join(fname, filename)
    reader = easyocr.Reader(['en'])
    imgH , imgW = image.shape[:2]#resmin boyutlarını alıyoruz. x,y,height,width bilgileri

    # Metinleri tanı
    result = reader.readtext(image)

    # Algılanan metinleri kare içine al ve orijinal resim üzerine çiz    
    for detection in result:
        points = detection[0]  # Algılanan metnin köşe noktalarını al

        min_coordinates = np.min(points, axis=0)
        max_coordinates = np.max(points, axis=0)
        x,y,w,h = int(min_coordinates[0]),int(min_coordinates[1]),int(max_coordinates[0]),int(max_coordinates[1]) 
        
        if (x - 15) < 0:
            x = 15

        cv2.rectangle(image,(x, y),(w, h),(0,0,255),3)#her harf için kutu çizdiriyoruz.
        cv2.putText(image,detection[1],(x,y+10),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),2)        
        
    cv2.imwrite(fname, image)
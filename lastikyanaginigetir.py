#Tüm lastik işlemlerini yapıp easyocr çalıştırırak sonuç almamızı sağlar.
from ultralytics import YOLO
import glob
import cv2
import os
import ocruygula as ocr
import numpy as np

path = "sample"

#Resimdeki lastik bulunan alanı kırpar
def crop(image,filename,tirecoordinate,jantcoordinate):
    x1 = int(tirecoordinate[0].item()) 
    y1 = int(tirecoordinate[1].item())
    x2 = int(tirecoordinate[2].item())
    y2 = int(tirecoordinate[3].item())+20

    oran = (x2-x1)/(y2-y1)
    if 0.9 < oran and oran < 1.1 : 
        cropped_image = image[y1:y2,x1:x2]

        fname = os.path.join(path, 'crop')
        if not os.path.exists(fname):
            os.mkdir(fname)

        fname = os.path.join(fname, filename)
        cv2.imwrite(fname,cropped_image)

        flatten_image = flat(cropped_image,filename)
        lastik_seridi = lastikseridinikirp(flatten_image,filename,tirecoordinate,jantcoordinate)
        ocr.detectocrtext(lastik_seridi,filename,path) 

#Lastiği düz şerit haline getirmeyi sağlar
def flat(image,filename):
    #flat
    w,h = image.shape[:2]    
    image = cv2.resize(image,(min(w, h),min(w, h)))
                
    # warpPolar fonksiyonunu kullanarak görüntüyü dönüştürme
    radius = w  # Dönüşümün merkezinden maksimum uzaklık
    warped_img = cv2.warpPolar(image, (0,0), (w  // 2, h // 2), radius, cv2.INTER_LINEAR + cv2.WARP_POLAR_LINEAR)        
    rotate_img = cv2.rotate(warped_img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    fname = os.path.join(path, 'flat')
    if not os.path.exists(fname):
        os.mkdir(fname)

    fname = os.path.join(fname, filename)
    cv2.imwrite(fname,rotate_img)
    #flat
    return rotate_img

def lastikseridinikirp(image,filename,tirecoordinate,jantcoordinate):
    w,h = image.shape[:2]  
    
    x1 = int(jantcoordinate[0].item()) 
    y1 = int(jantcoordinate[1].item())
    x2 = int(jantcoordinate[2].item())
    y2 = int(jantcoordinate[3].item())
    jantmaxlen = max((y2-y1),(x2-x1))
        
    fname = os.path.join(path, 'lastikseridi')
    if not os.path.exists(fname):
        os.mkdir(fname)
    
    fname = os.path.join(fname, filename)
    image = image[(int(w/2)-10):(w-int(jantmaxlen/2)),:]
    cv2.imwrite(fname,image)

    return image

    
def main():
    # loading a custom model
    model = YOLO('model/best_jantli.pt')

    for filename in os.listdir(path):
        if os.path.isdir(os.path.join(path, filename)) == False:            
            newpath = os.path.join(path, filename)
            image = cv2.imread(newpath)
            results = model.predict(image,conf=0.25,iou=0.45)
            results = results[0]
            copyimage = image.copy()
            hastire = False #lastik tespit etmezse o resim için işlem yapmamalı.jant,lastik 2 sınıf var. O yüzden bool değişkende tuttum            
            tirecoordinate = []
            jantcoordinate = []            
            for i in range(len(results.boxes)):
                box = results.boxes[i]
                conf = box.conf[0].item()
                class_id = int(box.cls[0].item())  # Get the class index (e.g., 0 or 1)
                class_name = results.names[class_id]  # Get the class name using the class index
                
                
                if class_name == "tires" and conf > 0.8: 
                    hastire = True
                    tirecoordinate = box.xyxy[0]
                
                if class_name == "jant":
                    jantcoordinate = box.xyxy[0]

                tensor = box.xyxy[0]
                x1 = int(tensor[0].item()) 
                y1 = int(tensor[1].item())
                x2 = int(tensor[2].item())
                y2 = int(tensor[3].item())
                
                label = class_name + " " + f"{conf:.2f}"

                cv2.rectangle(copyimage,(x1,y1),(x2,y2),(255,0,255),3)            
                cv2.putText(copyimage, label, (x1, y1-10), cv2.FONT_HERSHEY_COMPLEX, 3, (0,255,0), 5)
            
            detectfile = os.path.join(path, 'detect')
            if not os.path.exists(detectfile):
                os.mkdir(detectfile)

            fname = os.path.join(detectfile, filename)
            cv2.imwrite(fname,copyimage)

            if hastire == False:#Eğer lastik bulamadıysa return etsin
                continue
            
            crop(image,filename,tirecoordinate,jantcoordinate)             

main()
#Ortak kullandığım metodları burda yazdım
from ultralytics import YOLO
import os


#model = YOLO('model/best_jantli.pt')
model = YOLO('model/detect_yolov8_roboflow_tirejantdetectfromtrucktire_etiketlerdahadaraltildi.pt')
conf_value = 0.65


#işlem yapılacak dosya yolunun kullanıcıdan alınması
def getfilepath(text):    
    fpath = ""

    while True:
        print("\n\t\t\t***Çıkış için Q yada q basın.***\n\n")
        fpath = input(text)

        if(fpath == "q" or fpath == "Q"):
            fpath = ""
            break
        
        if not os.path.exists(fpath):
            print("!!!!!!!!!Girdiğiniz dosya yolu geçersiz.Lütfen geçerli bir dosya yolu giriniz.!!!!!!!!!\n\n")
        else:
            break
    return fpath


#Görüntüde lastik varmı kontrolü yaptığımız yer.
def hastire_inimage(image):
    hastire = False
    resulthastire = model.predict(image,conf=0.25,iou=0.45)
    resulthastire = resulthastire[0]

    for i in range(len(resulthastire.boxes)):
        boxhastire = resulthastire.boxes[i]
        confhastire = boxhastire.conf[0].item()
        class_idhastire = int(boxhastire.cls[0].item())  # Get the class index (e.g., 0 or 1)
        class_namehastire = resulthastire.names[class_idhastire]  # Get the class name using the class index

        if class_namehastire == "tires" and confhastire >= conf_value:
            hastire = True

    return hastire
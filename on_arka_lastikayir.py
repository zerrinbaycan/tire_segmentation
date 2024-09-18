# dosya yolundaki lastikleri ön lastik  arka lastik olarak iki klasörde ayırmamızı sağlar.
# Aynı zamanda lastiğin tamamının olmadığı resimleride siler

import os
import cv2
from ultralytics import YOLO

def onlastik_arkalastik_ayir(path):
    
    model = YOLO('model/best_jantli.pt')

    # Klasördeki dosyaların isimlerini al ve sadece resim dosyalarını seç
    resim_dosyalari = [dosya for dosya in os.listdir(path) if dosya.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    # Dosyaları saatine (modifikasyon zamanına) göre sıralama
    resim_dosyalari = sorted(resim_dosyalari, key=lambda dosya: os.path.getmtime(os.path.join(path, dosya)))

    # Sıralanmış dosya isimlerini ve saatlerini görüntüle
    onlastik= False
    arkalastik= False
    hastire = False
    for resim in resim_dosyalari: 
        newpath = os.path.join(path, resim)
        image = cv2.imread(newpath)
        results = model(image)
        results = results[0]
            
        for i in range(len(results.boxes)):
            box = results.boxes[i]
            conf = box.conf[0].item()
            class_id = int(box.cls[0].item())  # Get the class index (e.g., 0 or 1)
            class_name = results.names[class_id]  # Get the class name using the class index
            
            
            if class_name == "tires" and conf > 0.8:
                x1 = int(box.xyxy[0][0].item()) 
                y1 = int(box.xyxy[0][1].item())
                x2 = int(box.xyxy[0][2].item())
                y2 = int(box.xyxy[0][3].item())+20

                oran = (x2-x1)/(y2-y1)
                if 0.9 < oran and oran < 1.1 : #tam lastik bulmuş deme. yarısı görünen lastikleri ayırmak için
                    if (hastire == False and onlastik == False and arkalastik == False):
                        onlastik = True
                    elif (hastire == False and onlastik == True and arkalastik == False):
                        onlastik = False
                        arkalastik = True

                    hastire = True
                else:
                    hastire = False
                    
        if hastire == False:#Eğer lastik bulamadıysa resmi silsin
            os.remove(newpath)

        if hastire == True and onlastik == True:#Eğer lastik bulduysa ön arka lastik olarak kaydetsin
            fname = os.path.join(path, 'onlastik')
            if not os.path.exists(fname):
                os.mkdir(fname)

            fname = os.path.join(fname, resim)
            cv2.imwrite(fname,image)
            os.remove(newpath)

        if hastire == True and arkalastik == True:#Eğer lastik bulduysa ön arka lastik olarak kaydetsin
            fname = os.path.join(path, 'arkalastik')
            if not os.path.exists(fname):
                os.mkdir(fname)

            fname = os.path.join(fname, resim)
            cv2.imwrite(fname,image)
            os.remove(newpath)

#onlastik_arkalastik_ayir('02_09_2024_171544_34lcd762')            


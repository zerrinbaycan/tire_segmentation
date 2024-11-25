# Lastiğin olmadığı resimleri silmemizi sağlar
import os
import shutil 
from ultralytics import YOLO
import cv2
import datetime
import asama2_dosyalariyenidenadlandir as dosyayenidenadlandir

path_list = []
filecounter = 0
model = YOLO('model/best_jantli.pt')
conf_value = 0.65

#işlem yapılacak dosya yolunun kullanıcıdan alınması
def getfilepath():    
    fpath = ""

    while True:
        fpath = input("\n\t\t\t***Çıkış için Q yada q basın.***\n\nGörüntülerin dosya yolunu giriniz: ")

        if(fpath == "q" or fpath == "Q"):
            fpath = ""
            break
        
        if not os.path.exists(fpath):
            print("!!!!!!!!!Girdiğiniz dosya yolu geçersiz.Lütfen geçerli bir dosya yolu giriniz.!!!!!!!!!\n\n")
        else:
            break
    return fpath
        
#işleyeceğimiz resim dosyalarının yolunun listesini alıyoruz
def getpathlist(path):
    if os.path.isfile(path):
        path_list.append(path)
    else:
        for filename in os.listdir(path):
            if os.path.isdir(os.path.join(path, filename)):
                newpath = os.path.join(path, filename)
                getpathlist(newpath)
            else:
                file_extension = os.path.splitext(filename)[1].lower()                        
                if file_extension in ['.jpg', '.jpeg', '.png']:
                    path_list.append(os.path.join(path, filename))
    return path_list

#dosya yolundaki resimleri çekme
def load_images_from_folder(image_path,main_folder_path):
    global filecounter
    img =cv2.imread(image_path)#cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)
    
    if img is not None:
        results = model.predict(img,conf=0.25,iou=0.45)
        results = results[0]
        hastire = False
        for i in range(len(results.boxes)):
            box = results.boxes[i]
            conf = box.conf[0].item()
            class_id = int(box.cls[0].item())  # Get the class index (e.g., 0 or 1)
            class_name = results.names[class_id]  # Get the class name using the class index
                        
            if class_name == "tires" and conf >= conf_value: 
                hastire = True

        if hastire == False:#Eğer lastik bulamadıysa resmi silsin
            os.remove(image_path)

        

filepath = getfilepath()

if(filepath != ""):  
    # Dosyadan okuma yaparken 1.png,2.png sırasıyla okumuyor, 1.png,10.png,11.png sırasıyla alfabetik sırayla okuyor. 
    # Bunun için tüm işlemlerden önce 0001.png, 0002.png... gibi bi yöntem ile isimleri rename etmeyi düşündüm. Daha sonra dosya isimlendirmeyi bu hale getirirsem buna ihtiyaç kalmayacaktır.
    dosyayenidenadlandir.dosyalariisimlendir(filepath)

    bslnow = datetime.datetime.now()
    fname = bslnow.strftime("%Y_%m_%d_%H%M%S")
    print("Başlama zamanı: ",fname)
    
    getpathlist(filepath)    

    bitnow = datetime.datetime.now()
    fname = bitnow.strftime("%Y_%m_%d_%H%M%S")
    print("Bitiş zamanı: ",fname)

    resultfile = os.path.join(filepath, 'results')    

    if not os.path.exists(resultfile):
        os.mkdir(resultfile)
    else:#eğer kalsör varsa sil yeniden oluştur
        shutil.rmtree(resultfile)
        os.mkdir(resultfile)
    
    for path in path_list:
        load_images_from_folder(path,resultfile)

    









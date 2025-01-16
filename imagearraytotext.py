"""
import shutil
import cv2
import numpy as np
import os
import time
from PIL import Image
import commonfunctions as cf

def saveimagestotxt(images,folder_path):     
    #resimleri kaydedeceğimiz txt dosyasınıı oluştur        
    file_dir = os.path.join(folder_path, "npyfiles")
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    #resimleri kaydedeceğimiz txt dosyasınıı oluştur        
    i = 0
    while i < len(images):
        i += 1
        filename = os.path.join(file_dir, f"{i}.npy")    
        np.save(filename, images[i-1])      
        

def saveimages(folder_path): 
    try:    
        file_dir = os.path.join(folder_path, "txtfiles")
        if not os.path.exists(file_dir):
            return
        
        filenames = sorted(os.listdir(file_dir), key=lambda x: int(os.path.splitext(x)[0]))
        for filename in filenames:
            dosyaadi = os.path.splitext(filename)[0]
            path = os.path.join(file_dir,filename)
            array = np.load(path)
            image = Image.fromarray(array)  # NumPy array'i görüntüye çevir
            if image is not None and cf.hastire_inimage(image) == False:#Eğer lastik bulamadıysa resmi silsin        
                continue

            image.save(folder_path + "\\"+ dosyaadi+".png")  

        if os.path.exists(file_dir):
                shutil.rmtree(file_dir)
    except Exception as e:
        print(e)

# Klasörden resimleri okuyup tek bir array'e dönüştüren fonksiyon
def read_images_from_folder(folder_path):
    images = []
    filenames = sorted(os.listdir(folder_path), key=lambda x: int(os.path.splitext(x)[0]))
    for filename in filenames:
        img = cv2.imread(os.path.join(folder_path, filename), cv2.IMREAD_UNCHANGED)
        if img is not None:
            images.append(img)
    return np.array(images)

# Klasör yolunu belirtin
folder_path = 'D:\\evolog\\test\\07_11_2024_171859'


# Resimleri klasörden okuyun
images = read_images_from_folder(folder_path)

start_time = time.time()
saveimagestotxt(images,folder_path)
txt_time = time.time() - start_time
print("txt yazma süresi",txt_time)

start_time = time.time()
saveimages(folder_path)
change_time = time.time() - start_time
print("txt png'ye dönüştürme süresi",change_time)
"""




import shutil

import numpy as np
import commonfunctions as cf
import os
import cv2
import datetime
from PIL import Image

constantfile = "D:\\evolog\\test"

def saveimages(folder_path): 
    try:    
        file_dir = os.path.join(folder_path, "npyfiles")
        if not os.path.exists(file_dir):
            return
        
        filenames = sorted(os.listdir(file_dir), key=lambda x: int(os.path.splitext(x)[0]))
        for filename in filenames:
            dosyaadi = os.path.splitext(filename)[0]
            path = os.path.join(file_dir,filename)
            array = np.load(path)
            image = Image.fromarray(array)  # NumPy array'i görüntüye çevir
            if image is not None and cf.hastire_inimage(image) == False:#Eğer lastik bulamadıysa resmi silsin        
                continue

            image.save(folder_path + "\\"+ dosyaadi+".png")  

        if os.path.exists(file_dir):
                shutil.rmtree(file_dir)
    except Exception as e:
        print(e)
        
def checktire(filepath,imagefiles):
    try:            
        for file in imagefiles:        
            dosyaadi = os.path.join(filepath, file)
            img =cv2.imread(dosyaadi)

            if img is not None and cf.hastire_inimage(img) == False:#Eğer lastik bulamadıysa resmi silsin        
                os.remove(dosyaadi)

    except Exception as error:
        print("An exception occurred:",error)

# Parametre olarak gelen dosya yolundaki tüm dosya listesi alınır. Alt klasörlerin içinde dönebilmek için klasör dosya ayrımı yapılır.
# Dosyalarda lastik tespit ve aks ayrımı çalıştırılır. Varsa alt klasörler içinde dönülerek de bu işlemler tekrarlanır.
def iterate_folder_files(filepath):
    try:
        filelist = os.listdir(filepath)
        folders = [item for item in filelist if os.path.isdir(os.path.join(filepath, item)) and item != "AksBilgileri"]
        files = [item for item in filelist if os.path.isfile(os.path.join(filepath, item)) and (os.path.splitext(os.path.basename(item))[1]).lower() in ['.npy']]
        
        for fileitem in folders:
            if fileitem == "npyfiles":
                #saveimages(filepath)
                continue

            newfilepath = os.path.join(filepath, fileitem)
            iterate_folder_files(newfilepath)

    except Exception as error:
        print("An exception occurred:",error)

def main():
    try:
        gunsay = 1
        while gunsay >= 0:
            now = datetime.datetime.now() - datetime.timedelta(days=gunsay)
            yestarday = now.strftime("%Y_%m_%d")                
            filepath = os.path.join(constantfile, yestarday)               

            if(filepath != ""):  
                iterate_folder_files(filepath)   
            
            gunsay -= 1        

    except Exception as error:
        print("An exception occurred:",error)

main()

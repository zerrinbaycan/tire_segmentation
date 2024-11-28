# Lastiğin olmadığı resimleri silmemizi sağlar
import os
import shutil 
from ultralytics import YOLO
import cv2
import datetime
import asama2_dosyalariyenidenadlandir as dosyayenidenadlandir

path_list = []
model = YOLO('model/best_jantli.pt')
conf_value = 0.65

led_pixel_beginx = 548
led_pixel_beginy = 0
led_pixel_endx = 3548
led_pixel_endy = 3000
goruntudeki_lastik_orani = 2/3
aksfile = ""
last_aks_filenumber = 0#Aksbilgileri dosyasında oluşturulmuş en son aks dosya numarasını tutuyor
sonkaydedilenresim = 0
filename2 = 0

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

#En son oluşturulan klasör adını döner
def get_last_created_folder(parent_folder):
        # Klasör içindeki alt klasörlerin isimlerini al
        folders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]

        # Klasör isimlerini sayısal olarak sırala
        numeric_folders = sorted([int(folder) for folder in folders if folder.isdigit()])

        # En son oluşturulan klasör ismini döndür
        return numeric_folders[-1] if numeric_folders else 0


#dosya yolundaki resimleri çekme
def load_images_from_folder(image_path):
    global last_aks_filenumber
    global aksfile

    imgorg =cv2.imread(image_path)#cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)
    img = imgorg[:, led_pixel_beginx:led_pixel_endx]

    if img is not None:
        results = model.predict(img,conf=0.25,iou=0.45)
        results = results[0]

        for i in range(len(results.boxes)):
            box = results.boxes[i]
            conf = box.conf[0].item()
            class_id = int(box.cls[0].item())  # Get the class index (e.g., 0 or 1)
            class_name = results.names[class_id]  # Get the class name using the class index
            
            tensor = box.xyxy[0]
            x1 = int(tensor[0].item()) 
            y1 = int(tensor[1].item())
            x2 = int(tensor[2].item())
            y2 = int(tensor[3].item())
            oran = (x2-x1)/(y2-y1)
            
            if class_name == "tires" and conf >= conf_value and oran >= goruntudeki_lastik_orani: 
                file_name_with_extension = os.path.basename(image_path)
                file_name = os.path.splitext(file_name_with_extension)[0]
                
                last_aks_filenumber += 1
                aksfilename = os.path.join(aksfile, str(last_aks_filenumber))    
                if not os.path.exists(aksfile):
                    os.mkdir(aksfile)
                    
                    aksfile
                sonkaydedilenresim = 0
                
                if(filename1 <= 0 and filename2 <= 0):
                    filename1 = int(file_name)

def aks_ayrimicalistir(filepath,files,last_aks_filenumber,userakspath):
    picture_fileno = 0
    aksfilename = ""
    hastire = False

    for file in files:
        dosyaadi = os.path.join(filepath, file)
        imgorg =cv2.imread(dosyaadi)#cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)
        img = imgorg[:, led_pixel_beginx:led_pixel_endx]

        if img is not None:
            resulthastire = model.predict(imgorg,conf=0.25,iou=0.45)
            resulthastire = resulthastire[0]

            for i in range(len(resulthastire.boxes)):
                boxhastire = resulthastire.boxes[i]
                confhastire = boxhastire.conf[0].item()
                class_idhastire = int(boxhastire.cls[0].item())  # Get the class index (e.g., 0 or 1)
                class_namehastire = resulthastire.names[class_idhastire]  # Get the class name using the class index

                if class_namehastire == "tires" and confhastire >= conf_value:
                    hastire = True
            if hastire == False:#Eğer lastik bulamadıysa resmi silsin
                os.remove(dosyaadi)
                continue

            results = model.predict(img,conf=0.25,iou=0.45)
            results = results[0]

            for i in range(len(results.boxes)):
                box = results.boxes[i]
                conf = box.conf[0].item()
                class_id = int(box.cls[0].item())  # Get the class index (e.g., 0 or 1)
                class_name = results.names[class_id]  # Get the class name using the class index
                
                if class_name == "tires" and conf >= conf_value:
                    hastire = True

                tensor = box.xyxy[0]
                x1 = int(tensor[0].item()) 
                y1 = int(tensor[1].item())
                x2 = int(tensor[2].item())
                y2 = int(tensor[3].item())
                oran = (x2-x1)/(y2-y1)
                
                if class_name == "tires" and conf >= conf_value and oran >= goruntudeki_lastik_orani: 
                    file_name_with_extension = os.path.basename(dosyaadi)
                    file_name = os.path.splitext(file_name_with_extension)[0]
                    
                    if(int(file_name) - picture_fileno > 3):                        
                        last_aks_filenumber += 1
                        aksfilename = os.path.join(userakspath, str(last_aks_filenumber))    

                        if not os.path.exists(aksfilename):
                            os.mkdir(aksfilename)
                    
                    picture_fileno = int(file_name)

                    aks_imgname = os.path.join(aksfilename, file)    
                    cv2.imwrite(aks_imgname, img)

                    akstxtpath = os.path.join(userakspath, 'AksBilgileri.txt')    
                    with open(akstxtpath, 'a') as aksfile:
                        dosyametni = str(last_aks_filenumber) + " | " + dosyaadi + " | \n"
                        aksfile.write(dosyametni)  # Dosya otomatik olarak kapanır

                        
                    
                       

def dosyalarda_don(filepath,userakspath):
    filelist = os.listdir(filepath)
    folders = [item for item in filelist if os.path.isdir(os.path.join(filepath, item)) and item != "AksBilgileri"]
    files = [item for item in filelist if os.path.isfile(os.path.join(filepath, item)) and (os.path.splitext(os.path.basename(item))[1]).lower() in ['.jpg', '.jpeg', '.png']]

    sorted_files = sorted(files, key=lambda x: int(os.path.splitext(x)[0]))

    if(len(sorted_files) > 0):
        last_aks_filenumber = get_last_created_folder(userakspath)
        aks_ayrimicalistir(filepath,sorted_files,last_aks_filenumber,userakspath)
    
    for fileitem in folders:
        newfilepath = os.path.join(filepath, fileitem)
        dosyalarda_don(newfilepath,userakspath)

def main():
    try:
        akspath = getfilepath("!!!!Seçtiğiniz dosya yoluna AksBilgileri klasörü açılıp, bu klasör içine dosyalar kaydedilecektir.!!!!\nAks bilgilerinin kaydedileceği yolu giriniz: ")
        filepath = getfilepath("Görüntülerin dosya yolunu giriniz: ")

        #AksBilgileri klasörünün oluşturulması
        userakspath = os.path.join(akspath, 'AksBilgileri')    
        if not os.path.exists(userakspath):
            os.mkdir(userakspath)

        txtpath = os.path.join(userakspath, 'AksBilgileri.txt')    
        if not os.path.exists(txtpath):
            with open(txtpath, 'w') as file:
                pass

        if(filepath != ""):  
            # Dosyadan okuma yaparken 1.png,2.png sırasıyla okumuyor, 1.png,10.png,11.png sırasıyla alfabetik sırayla okuyor. 
            # Bunun için tüm işlemlerden önce 0001.png, 0002.png... gibi bi yöntem ile isimleri rename etmeyi düşündüm. Daha sonra dosya isimlendirmeyi bu hale getirirsem buna ihtiyaç kalmayacaktır.
            #dosyayenidenadlandir.dosyalariisimlendir(filepath)
            #getpathlist(filepath)

            dosyalarda_don(filepath,userakspath)   
            
    except Exception as error:
        print("An exception occurred:",error)

main()
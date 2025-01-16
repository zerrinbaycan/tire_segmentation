# Bu py dosyası ile aşağıdaki adımları gerçekleştiriyoruz.
# Aks bilgileri kasörü içinde gezip aynı isimle klasör oluşturup sadece lastik olan alanları crop etmeyi sağlar.

import commonfunctions as cf
import os
import cv2
import constants as c

#bu metod crop edilen lastiğin size bilgisine göre resmi kare yapmak için siyah pixeller ekleyip kare resim döndürür 
def resmiduzenle(img):
    height, width = img.shape[:2]

    maxlen = max(height,width)
    if width > height:
        img = cv2.copyMakeBorder(img, maxlen-height, 0, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    else:
        img = cv2.copyMakeBorder(img,0, 0,  maxlen-width, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    
    return img    

#akslara göre klasörlenen dosyalar içinde dönerek lastik olan koordinaların crop edilip büyük olan kenara göre siyah piksellerle tamamlanarak kare bir resim oluşturulması
def axletirecrop(filepath,files,userakspath,txtpath):
    try:   
        dosyaadi  = ""
        for file in files:       
            dosyaadi = os.path.join(filepath, file)
            try:                 
                img =cv2.imread(dosyaadi)                

                if img is not None:
                    results = cf.model.predict(img,conf=0.25,iou=0.45)
                    results = results[0]

                    detected_tirecount = 0
                    tamlastikvar = False
                    tirecoordinate = []
                    for i in range(len(results.boxes)):
                        box = results.boxes[i]
                        conf = box.conf[0].item()
                        class_id = int(box.cls[0].item())  # Get the class index (e.g., 0 or 1)
                        class_name = results.names[class_id]  # Get the class name using the class index
                        
                        points = box.xyxy[0]
                        x1 = int(points[0].item()) 
                        y1 = int(points[1].item())
                        x2 = int(points[2].item())
                        y2 = int(points[3].item())
                        oran = (x2-x1)/(y2-y1)
                        if class_name == "tires" and conf >= c.conf_value:
                            detected_tirecount += 1
                        if class_name == "tires" and conf >= c.conf_value and oran >= c.goruntudeki_lastik_orani: 
                            tamlastikvar = True
                            tirecoordinate = points

                    if(tamlastikvar == True):#if(detected_tirecount == 1 and tamlastikvar == True):
                        img = resmiduzenle(img[int(tirecoordinate[1].item()):int(tirecoordinate[3].item()), int(tirecoordinate[0].item()):int(tirecoordinate[2].item())])
                        cropdosyaadi = os.path.join(userakspath, file)
                        cv2.imwrite(cropdosyaadi,img)
                           
                        with open(txtpath, 'a') as aksfile:
                            dosyametni = os.path.basename(userakspath) + " | " + dosyaadi + " | \n"
                            aksfile.write(dosyametni)  # Dosya otomatik olarak kapanır
            except :
                os.remove(dosyaadi) #Hatalı,açılmayan resim dosyaları vardı bunları sildim                       
                continue
    except Exception as e:
        print("dosya hatası :",dosyaadi,e ) 


# Parametre olarak gelen dosya yolundaki tüm dosya listesi alınır. Alt klasörlerin içinde dönebilmek için klasör dosya ayrımı yapılır.
# Dosyalardan ortadaki resmi bulur crop metodu çalıştırılır. Varsa alt klasörler içinde dönülerek de bu işlemler tekrarlanır.
def iterate_folder_files(filepath,userakspath,txtpath):
    filelist = os.listdir(filepath)
    folders = [item for item in filelist if os.path.isdir(os.path.join(filepath, item)) and item not in "AksBilgileri"]
    files = [item for item in filelist if os.path.isfile(os.path.join(filepath, item)) and (os.path.splitext(os.path.basename(item))[1]).lower() in ['.jpg', '.jpeg', '.png']]

    folders = sorted(folders, key=lambda x: int(os.path.splitext(x)[0]))
    #Dosya isimlerimiz numerik olduğu için bir sıralama yapıyoruz. Aksları doğru sınıflandırmak için bu gerekli.
    sorted_files = sorted(files, key=lambda x: int(os.path.splitext(x)[0]))

    if(len(sorted_files) > 0):
        aksfilename = os.path.basename(filepath)
        temp_userakspath = os.path.join(userakspath, aksfilename)    
        if not os.path.exists(temp_userakspath):
            os.mkdir(temp_userakspath)
        
        index = round(len(sorted_files)/2)
        tmptext = sorted_files[index-1]
        newsorted_files = [tmptext]
        axletirecrop(filepath,sorted_files,temp_userakspath,txtpath)
    
    for fileitem in folders:
        newfilepath = os.path.join(filepath, fileitem)
        iterate_folder_files(newfilepath,userakspath,txtpath)

def main():
    try:
        akspath = cf.getfilepath("!!!!Seçtiğiniz dosya yoluna AksBilgileri_crop klasörü açılıp, bu klasör içine dosyalar kaydedilecektir.!!!!\nAks bilgilerinin kaydedileceği yolu giriniz: ")#yeni dosyaları kaydedeceğimiz yol girilicek
        filepath = cf.getfilepath("İşlem yapılacak görüntülerin dosya yolunu giriniz: ")#Buraya aks bilgileri kalsör yolu girilecek

        #AksBilgileri klasörü ve txt dosyasının oluşturulması
        userakspath = os.path.join(akspath, 'AksBilgileri_crop')    
        if not os.path.exists(userakspath):
            os.mkdir(userakspath)

        txtpath = os.path.join(userakspath, 'AksBilgileri_crop.txt')    
        if not os.path.exists(txtpath):
            with open(txtpath, 'w') as file:
                pass

        if(filepath != ""):  
            iterate_folder_files(filepath,userakspath,txtpath)   
            
    except Exception as error:
        print("An exception occurred:",error)

main()


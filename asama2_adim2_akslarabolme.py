# Bu py dosyası ile aşağıdaki adımları gerçekleştiriyoruz.
# 1. Verilen dosya yolunda lastik bulunmayan resimleri siliyoruz.
# 2. Görüntüde lastik varsa belirlenen pixel aralığında lastiğin %60 kısmı varmı kontrolü yapıyoruz. Varsa bu dosya içindeki resimleri akslara bölüyoruz. 

import commonfunctions as cf
import os
import cv2
import constants as c

#En son oluşturulan klasör adını döner
def getlast_created_folder(parent_folder):
        # Klasör içindeki alt klasörlerin isimlerini döner
        folders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]

        # Klasör isimlerini sayısal olarak sıralar
        numeric_folders = sorted([int(folder) for folder in folders if folder.isdigit()])

        # En son oluşturulan klasör ismini döndür
        return numeric_folders[-1] if numeric_folders else 0

#dosya yolundaki resimlerde lastik yoksa resmi sil, varsa akslara göre kalsörle
def aks_ayrimicalistir(filepath,files,last_aks_filenumber,userakspath):
    try:
        picture_fileno = 0
        aksfilename = ""    
        dosyaadi  = ""
        """
        last_folder = os.path.basename(filepath)             
        with open(os.path.join(userakspath, 'IslemYapilanDosyalar.txt')  , "r", encoding="utf-8") as islemfile:
            found = False
            for line in islemfile:
                if last_folder in line:
                    found = True                
                    break  # Bulunduğu anda durdur (isteğe bağlı)

        if found:
            return
        """
        for file in files:       
            dosyaadi = os.path.join(filepath, file)
            try:                 
                imgorg =cv2.imread(dosyaadi)#cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)
                img = imgorg[:, c.led_pixel_beginx:c.led_pixel_endx]

                if img is not None:
                    #Orjinal boyuttaki resimde lastik varmı bakıyoruz. Yoksa resmi silip diğer resme geçiyoruz.
                    ################Lasitk yoksa sil bloğu
                    if cf.hastire_inimage(imgorg) == False:#Eğer lastik bulamadıysa resmi silsin
                        os.remove(dosyaadi)
                        continue
                    ################

                    results = cf.model.predict(img,conf=0.25,iou=0.45)
                    results = results[0]

                    detected_tirecount = 0
                    tamlastikvar = False
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
                        """
                        if class_name == "tires" and conf >= c.conf_value and oran >= c.goruntudeki_lastik_orani: 
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
                        """
                        if class_name == "tires" and conf >= c.conf_value:
                            detected_tirecount += 1
                        if class_name == "tires" and conf >= 0.8 and oran >= c.goruntudeki_lastik_orani: 
                            tamlastikvar = True

                    if(tamlastikvar == True):#if(detected_tirecount == 1 and tamlastikvar == True):
                        file_name_with_extension = os.path.basename(dosyaadi)
                        file_name = os.path.splitext(file_name_with_extension)[0]
                        
                        fark = 5
                        if(detected_tirecount > 1):
                            fark = 3
                        if(int(file_name) - picture_fileno > fark or picture_fileno == 0):                        
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
            except :
                os.remove(dosyaadi) #Hatalı,açılmayan resim dosyaları vardı bunları sildim                       
                continue
    except Exception as e:
        print("dosya hatası :",dosyaadi,e )    

def fileprocess_isok(dosya_yolu, aranacak_metin):
    textfound = False
    try:
        # Dosyayı okuma modunda aç
        with open(dosya_yolu, 'r', encoding='utf-8') as processfile:
            for satir_no, satir in enumerate(processfile, start=1):
                # Aranacak metni kontrol et
                if aranacak_metin in satir:
                    textfound = True
        print("Arama tamamlandı.")
    except FileNotFoundError:
        print(f"Dosya bulunamadı: {dosya_yolu}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

    return textfound

# Parametre olarak gelen dosya yolundaki tüm dosya listesi alınır. Alt klasörlerin içinde dönebilmek için klasör dosya ayrımı yapılır.
# Dosyalarda lastik tespit ve aks ayrımı çalıştırılır. Varsa alt klasörler içinde dönülerek de bu işlemler tekrarlanır.
def iterate_folder_files(filepath,userakspath):
    filelist = os.listdir(filepath)
    folders = [item for item in filelist if os.path.isdir(os.path.join(filepath, item)) and item != "AksBilgileri"]
    files = [item for item in filelist if os.path.isfile(os.path.join(filepath, item)) and (os.path.splitext(os.path.basename(item))[1]).lower() in ['.jpg', '.jpeg', '.png']]

    #Dosya isimlerimiz numerik olduğu için bir sıralama yapıyoruz. Aksları doğru sınıflandırmak için bu gerekli.
    sorted_files = sorted(files, key=lambda x: int(os.path.splitext(x)[0]))

    if(len(sorted_files) > 0):
        last_aks_filenumber = getlast_created_folder(userakspath)#Aksbilgileri dosyasında oluşturulmuş en son aks dosya numarasını çekiyoruz
        aks_ayrimicalistir(filepath,sorted_files,last_aks_filenumber,userakspath)
    
    for fileitem in folders:
        islemtxt = os.path.join(userakspath, 'IslemYapilanDosyalar.txt')            
        if fileprocess_isok(islemtxt, fileitem):
        #if(fileitem == "2024_10_31" or fileitem =="2024_10_25" or fileitem =="2024_10_26" or fileitem =="2024_10_27" or fileitem =="2024_10_28" or fileitem =="2024_10_30"):
            continue

        newfilepath = os.path.join(filepath, fileitem)
        iterate_folder_files(newfilepath,userakspath)

def main():
    try:
        akspath = cf.getfilepath("!!!!Seçtiğiniz dosya yoluna AksBilgileri klasörü açılıp, bu klasör içine dosyalar kaydedilecektir.!!!!\nAks bilgilerinin kaydedileceği yolu giriniz: ")
        filepath = cf.getfilepath("İşlem yapılacak görüntülerin dosya yolunu giriniz: ")

        #AksBilgileri klasörü ve txt dosyasının oluşturulması
        userakspath = os.path.join(akspath, 'AksBilgileri')    
        if not os.path.exists(userakspath):
            os.mkdir(userakspath)

        txtpath = os.path.join(userakspath, 'AksBilgileri.txt')    
        if not os.path.exists(txtpath):
            with open(txtpath, 'w') as file:
                pass
        """
        islemyapilandosyalar = os.path.join(userakspath, 'IslemYapilanDosyalar.txt')    
        if not os.path.exists(txtpath):
            with open(txtpath, 'w') as file:
                pass
        """
        if(filepath != ""):  
            iterate_folder_files(filepath,userakspath)   
            
    except Exception as error:
        print("An exception occurred:",error)

main()


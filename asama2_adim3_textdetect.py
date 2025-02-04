#bu metod lastik üzerindeki yazı bulunan alanları detect edip yazılı alanları ayrı bir dosyaya kaydetmeyi sağlar
#bunu çalıştırmadan önce lastik akslara bölme çalıştırılmalıdır. Akslara bölünmüş lastikde aşağıdaki işlemler yapılmalıdır.
import commonfunctions as cf
import os
import cv2
import lastikislemleri as li
import ocruygula as ocr

last_filenumber = 0

#En son oluşturulan klasör adını döner
def getlast_created_folder(parent_folder):
    global last_filenumber
    try:
        fpath = os.path.join(parent_folder, 'crop')  
        filelist = os.listdir(fpath)        
        files = [item for item in filelist if os.path.isfile(os.path.join(fpath, item)) and (os.path.splitext(os.path.basename(item))[1]).lower() in ['.jpg', '.jpeg', '.png']]        
        sorted_files = sorted(files, key=lambda x: int(os.path.splitext(x)[0]))

        # En son oluşturulan klasör ismini döndür
        return int(os.path.splitext(sorted_files[-1])[0])  if len(sorted_files) > 0 else 0
    except Exception as error:
        last_filenumber = 0
        print("An exception occurred:",error)

def lastikislemlericalistir(filepath,sorted_files,detectedtextpath):
    global last_filenumber
    try:
        for file in sorted_files:       
            dosyaadi = os.path.join(filepath, file)
            try:
                img = cv2.imread(dosyaadi)
                if img is not None:
                    results = cf.model.predict(img,conf=0.25,iou=0.45)
                    results = results[0]
                    copyimage = img.copy()
                    tirecoordinate = []
                    jantcoordinate = []            
                    for i in range(len(results.boxes)):
                        box = results.boxes[i]
                        conf = box.conf[0].item()
                        class_id = int(box.cls[0].item())  # Get the class index (e.g., 0 or 1)
                        class_name = results.names[class_id]  # Get the class name using the class index

                        #görüntüde lastiğin bir kısmı olan alan kalmışsa burayıda lastik diye tespit ediyor unu önlemek için oranı ekledim
                        x1 = int(box.xyxy[0][0].item()) 
                        y1 = int(box.xyxy[0][1].item())
                        x2 = int(box.xyxy[0][2].item())
                        y2 = int(box.xyxy[0][3].item())+20

                        #detect edilen nesnenin genişliği ile yüksekliğini oranlıyoruz.Tam lastik ya da jant elde etmiş olmalıyız.Yarım olanların koordinatlarını göndermemek için
                        oran = (x2-x1)/(y2-y1)
                                                
                        if class_name == "tire" and conf > 0.8 and 0.9 < oran and oran < 1.1: 
                            tirecoordinate = box.xyxy[0]
                        
                        if class_name == "jant" and 0.9 < oran and oran < 1.1:
                            jantcoordinate = box.xyxy[0]
                        
                        label = class_name + " " + f"{conf:.2f}"

                        cv2.rectangle(copyimage,(x1,y1),(x2,y2),(255,0,255),3)            
                        cv2.putText(copyimage, label, (x1, y1-10), cv2.FONT_HERSHEY_COMPLEX, 3, (0,255,0), 5)
                    if len(tirecoordinate) > 0:
                        detectfile = os.path.join(detectedtextpath, 'detect')
                        if not os.path.exists(detectfile):
                            os.mkdir(detectfile)

                        detectfile = os.path.join(detectfile, (str(last_filenumber) + os.path.splitext(file)[1]))
                        cv2.imwrite(detectfile,copyimage)
                        last_filenumber += 1
                                        
                    if len(tirecoordinate) <= 0:
                        continue
                    last_filenumber = li.lastikislemleri(img,filepath,file,tirecoordinate,jantcoordinate,detectedtextpath,last_filenumber)
                
            except:
                os.remove(dosyaadi) #Hatalı,açılmayan resim dosyaları vardı bunları sildim                       
                continue
    except Exception as error:
        print("An exception occurred:",error)

def iterate_folder_files(filepath,detectedtextpath):
    global last_filenumber
    try:
        filelist = os.listdir(filepath)
        folders = [item for item in filelist if os.path.isdir(os.path.join(filepath, item)) and item != "AksBilgileri" and item != "DetectedText" and item != "results"]
        files = [item for item in filelist if os.path.isfile(os.path.join(filepath, item)) and (os.path.splitext(os.path.basename(item))[1]).lower() in ['.jpg', '.jpeg', '.png']]

        #Dosya isimlerimiz numerik olduğu için bir sıralama yapıyoruz. Aksları doğru sınıflandırmak için bu gerekli.
        sorted_files = sorted(files, key=lambda x: int(os.path.splitext(x)[0]))

        if(len(sorted_files) > 0):
            lastikislemlericalistir(filepath,sorted_files,detectedtextpath)
        
        for fileitem in folders:
            newfilepath = os.path.join(filepath, fileitem)
            iterate_folder_files(newfilepath,detectedtextpath)
    except Exception as error:
        print("An exception occurred:",error)

def main():
    global last_filenumber
    try:
        path1 = cf.getfilepath("!!!!Seçtiğiniz dosya yoluna DetectedText klasörü açılıp, bu klasör içine text tespit edilmiş görüntüler kaydedilecektir.!!!!\nDetectedText klasör yolu giriniz: ")
        filepath = cf.getfilepath("İşlem yapılacak görüntülerin dosya yolunu giriniz: ")

        #AksBilgileri klasörü ve txt dosyasının oluşturulması
        detectedtextpath = os.path.join(path1, 'DetectedText')    
        if not os.path.exists(detectedtextpath):
            os.mkdir(detectedtextpath)

        txtpath = os.path.join(detectedtextpath, 'DetectedText.txt')    
        if not os.path.exists(txtpath):
            with open(txtpath, 'w') as file:
                pass
        getlast_created_folder(detectedtextpath)
        if(filepath != ""):  
            iterate_folder_files(filepath,detectedtextpath)   
            
    except Exception as error:
        print("An exception occurred:",error)

main()
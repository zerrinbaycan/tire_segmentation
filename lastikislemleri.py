import os
import cv2
import numpy as np
import easyocr
#import Tireclass 
import deepOCR

reportrow = ""

def lastikislemleri(img,mainfilepath,filename,tirecoordinate,jantcoordinate,detectedtextpath,last_filenumber):
    global reportrow
    try:
        reportrow = ""
        #lastik olan alanın crop edilmesi
        x1 = int(tirecoordinate[0].item()) 
        y1 = int(tirecoordinate[1].item())
        x2 = int(tirecoordinate[2].item())
        y2 = int(tirecoordinate[3].item())+20

        #lastiğin genişliği ile yüksekliğini oranlıyoruz.Tam lastik elde etmiş olmak düzleştirme için önemli olduğundan bunu yaptık.
        oran = (x2-x1)/(y2-y1)
        if 0.9 < oran and oran < 1.1 : 
            last_filenumber += 1
            cropped_image = img[y1:y2,x1:x2]
            croppedfile = os.path.join(detectedtextpath, 'crop')
            if not os.path.exists(croppedfile):
                os.mkdir(croppedfile)
            
            fname = (str(last_filenumber) + os.path.splitext(filename)[1])

            croppedfilepath = os.path.join(croppedfile, fname)
            cv2.imwrite(croppedfilepath,cropped_image)

            reportrow = "org_filepath: {} | ".format(os.path.join(mainfilepath, filename))
                                                       
            flatten_image = tireflat(cropped_image,fname,detectedtextpath)
            lastik_seridi = lastikseridinikirp(flatten_image,fname,tirecoordinate,jantcoordinate,detectedtextpath)
            detectocrtext(lastik_seridi,fname,detectedtextpath)           

        return last_filenumber
    except Exception as error:
        print("An exception occurred:",error)

#Lastiği düz şerit haline getirmeyi sağlar
def tireflat(img,filename,detectedtextpath):
    try:                
        w,h = img.shape[:2]    
        img = cv2.resize(img,(min(w, h),min(w, h)))
                    
        # warpPolar fonksiyonunu kullanarak görüntüyü dönüştürme
        radius = w  # Dönüşümün merkezinden maksimum uzaklık
        warped_img = cv2.warpPolar(img, (0,0), (w  // 2, h // 2), radius, cv2.INTER_LINEAR + cv2.WARP_POLAR_LINEAR)        
        rotate_img = cv2.rotate(warped_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        flattire = os.path.join(detectedtextpath, 'flattire')
        if not os.path.exists(flattire):
            os.mkdir(flattire)

        flattire_dir = os.path.join(flattire, filename) 
        cv2.imwrite(flattire_dir,rotate_img)
        return rotate_img    
    except Exception as error:  
        print("An exception occurred:",error)

def lastikseridinikirp(img,fname,tirecoordinate,jantcoordinate,detectedtextpath):
    global reportrow
    try:
        w,h = img.shape[:2]  
    
        x1 = int(jantcoordinate[0].item()) 
        y1 = int(jantcoordinate[1].item())
        x2 = int(jantcoordinate[2].item())
        y2 = int(jantcoordinate[3].item())
        jantmaxlen = max((y2-y1),(x2-x1))
            
        filepath = os.path.join(detectedtextpath, 'lastikseridi')
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        
        filepath = os.path.join(filepath, fname)
        img = img[(int(w/2)-10):(w-int(jantmaxlen/2)),:]
        cv2.imwrite(filepath,img)
        
        reportrow += "flattire_path: {} | ".format(filepath)
        return img
    except Exception as error:
        print("An exception occurred:",error)

def detectocrtext(img,filename,detectedtextpath):
    global reportrow
    try:        
        ocr = os.path.join(detectedtextpath, 'OCR')
        if not os.path.exists(ocr):
            os.mkdir(ocr)
        
        textimages = os.path.join(detectedtextpath, 'textimages')
        if not os.path.exists(textimages):
            os.mkdir(textimages)

        reader = easyocr.Reader(['en'])
        imgH , imgW = img.shape[:2]#resmin boyutlarını alıyoruz. x,y,height,width bilgileri

        # Metinleri tanı
        result = reader.readtext(img)

        # Algılanan metinleri kare içine al ve orijinal resim üzerine çiz
        i = 0
        imagecopy = img.copy() 

        resultrow = reportrow
        for detection in result:
            resultrow = ""
            points = detection[0]  # Algılanan metnin köşe noktalarını al

            min_coordinates = np.min(points, axis=0)
            max_coordinates = np.max(points, axis=0)
            x,y,w,h = int(min_coordinates[0]),int(min_coordinates[1]),int(max_coordinates[0]),int(max_coordinates[1]) 

            i += 1
            if (x - 15) < 0:
                x = 15
            
            if(y - 15) < 0:
                y = 15
            yaziolan_alan = imagecopy[y-15:h+15,x-15:w+15]
            findtext = detection[1]
            #bulduğu metin içerisinde \/:*?"<> işaretleri varsa dosya isminde bunlar olmaması gerektiğinden resmi kaydedemiyor. 
            #Bende bu yüzden 'türkçeadı' ile kaydettim. Ör: Bulduğu text  W"tr?   ise W'çifttırnak'tr'soruişareti' şeklinde kaydedicem        
            findtext = findtext.replace('\\', '\'slash\'')
            findtext = findtext.replace('/', '\'tersslash\'')
            findtext = findtext.replace(':', '\'ikinokta\'')
            findtext = findtext.replace('*', '\'yıldız\'')
            findtext = findtext.replace('?', '\'soruişareti\'')
            findtext = findtext.replace('"', '\'çifttırnak\'')
            findtext = findtext.replace('<', '\'küçüktür\'')
            findtext = findtext.replace('>', '\'büyüktür\'')

            isim = textimages + "\\{}_tireflatname_{}_{}".format(findtext,str(i),filename)            
            cv2.imwrite(isim, yaziolan_alan) 

            deepocrtext = deepOCR.deepOCR(yaziolan_alan)
            resultrow = reportrow + "textimages_path: {} | deepOCRtext: {} | easyOCRconfidence: {} | find_easyocr: {} |   \n".format(isim,deepocrtext,detection[2],detection[1])
            
            cv2.rectangle(img,(x, y),(w, h),(0,0,255),3)#her harf için kutu çizdiriyoruz.
            cv2.putText(img,detection[1],(x,y+10),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),2)               
        
        focr_dir = os.path.join(ocr, filename)
        cv2.imwrite(focr_dir, img)
        
        with open(os.path.join(detectedtextpath, "DetectedText.txt"), 'a') as txtfile:
                txtfile.write(resultrow)  # Dosya otomatik olarak kapanır

    except Exception as error:
        print("An exception occurred:",error)




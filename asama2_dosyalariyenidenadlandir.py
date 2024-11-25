# Dosya isimlerini 4 haneli sıralamaya çevirmemizi sağlar(0001.png, 0002.png... gibi). 
# Dosyadan okuma yaparken 1.png,2.png sırasıyla okumuyor, 1.png,10.png,11.png sırasıyla alfabetik sırayla okuyor. 
# Bunun için tüm işlemlerden önce böyle bi yöntem ile sıralama yapmayı düşündüm. Daha sonra dosya isimlendirmeyi bu hale getirirsem buna ihtiyaç kalmayacaktır.
import os

def dosyalariisimlendir(filepath):
    for filename in os.listdir(filepath):
        if os.path.isdir(os.path.join(filepath, filename)):
                newpath = os.path.join(filepath, filename)
                dosyalariisimlendir(newpath)
        else:
            name, extension = os.path.splitext(filename)
            new_name = f"{int(name):04d}{extension}"
            oldpath = os.path.join(filepath, filename)
            newpath = os.path.join(filepath, new_name)
            print("{0} {1}  {2}".format(name, extension,new_name))
            os.rename(oldpath, newpath) 


        
    
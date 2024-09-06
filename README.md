# Lastik yanak kısmının düz şerit halinde elde edilmesi
* Lastik ve jant poligon olarak etiketlenerek yolov8 ile eğitildi ve model oluşturuldu. 
* Bu model ile detection yapılarak %80 oranında bulunan lastikler için aşağıdaki maddeler çalıştırıldı.
    - Resimde sadece lastik olan alan yeni bir resim olarak crop dosyasına kaydedildi.

    - Sadece lastik olan alan alındığında yaklaşık olarak kare şeklinde bir resim elde edilmiş oldu. Resmin  width-height bilgisinden min olan değere resize edildi. warpPolar metodu ile yuvarlak şekil orta noktasından açılarak düz hale getirilip flat dosyasına kaydedildi.

    - Detection yapılırken jantın bulunduğu koordinat bilgiside tespit ediliyordu. Bu koordinat bilgisinden şerit haline getirilen lastikten jant bulunan alan çıkarıldı ve lastikseridi dosyasına kaydedildi. 

    -Bu görüntü easyocr'a verilerek text detection ve recognition yapıldı. Sonuç OCR dosyasına kaydedildi.
from ultralytics import YOLO
import cv2
import numpy as np

# YOLOv8 modelini yükle
model = YOLO('model/best.pt') # YOLOv8'in segmentasyon modelini kullanıyoruz

# Görüntüyü yükle
image_path = "C:\\ZerrinGit\\basler_mono\\images\\02_09_2024_190452_34gfs410\\52.png"
image = cv2.imread(image_path)

# Modeli görüntü üzerinde çalıştır
results = model(image)

# Sonuçları ve maskeleri kontrol edin
for result in results:
    print("Detection results:", result)
    
    if result.masks is not None and len(result.masks) > 0:  # Maskelerin varlığını kontrol edin
        masks = result.masks
        for mask in masks:
            mask_array = mask.cpu().numpy()  # Maskeyi NumPy dizisine dönüştür
            mask_image = (mask_array * 255).astype(np.uint8)  # 0-1 arasında olan değerleri 0-255 aralığına çek
            cv2.imshow("Mask", mask_image)  # Maskeyi görüntüle
            cv2.waitKey(0)  # Bir tuşa basılmasını bekleyin
            cv2.destroyAllWindows()  # Pencereyi kapatın
    else:
        print("No masks found in the image or the masks are empty.")
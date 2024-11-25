import cv2
from ultralytics import YOLO
import numpy as np

imgorg = cv2.imread("sample\\lastikseridi\\25.png")
model = YOLO('model\\best_yolov8_text_detection.pt')

image = imgorg.copy()
results = model(image)
for result in results[0].boxes:  # results[0] üzerinde çalış
    bbox = result.xyxy[0].cpu().numpy()  # Bounding box koordinatları (x1, y1, x2, y2)
    x1, y1, x2, y2 = map(int, bbox)  # Koordinatları tam sayıya çevir
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Bounding box çiz (yeşil renk)
cv2.imwrite("yontem1_yolov8.png",image)


image = imgorg.copy()
h, w = image.shape[:2]
maxlen = max(h,w)

results = model(image,imgsz = maxlen)
for result in results[0].boxes:  # results[0] üzerinde çalış
    bbox = result.xyxy[0].cpu().numpy()  # Bounding box koordinatları (x1, y1, x2, y2)
    x1, y1, x2, y2 = map(int, bbox)  # Koordinatları tam sayıya çevir
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Bounding box çiz (yeşil renk)
cv2.imwrite("yontem2_yolov8.png",image)


canvas = np.zeros((maxlen, maxlen, 3), dtype=np.uint16)
image = imgorg.copy()

# Resmi merkeze yerleştirmek için hesaplama
x_offset = (maxlen - w) // 2
y_offset = (maxlen - h) // 2


# Y ekseninde boşluk miktarını hesapla
padding_height = maxlen - h

# Y ekseninde alt kısma siyah boşluk eklemek için padding oluştur (üstte 0, altta padding_height kadar ekle)
padded_image = cv2.copyMakeBorder(image, 0, padding_height, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])


results = model(padded_image)

for result in results[0].boxes:  # results[0] üzerinde çalış
    bbox = result.xyxy[0].cpu().numpy()  # Bounding box koordinatları (x1, y1, x2, y2)
    x1, y1, x2, y2 = map(int, bbox)  # Koordinatları tam sayıya çevir
    cv2.rectangle(padded_image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Bounding box çiz (yeşil renk)

cv2.imwrite("yontem3_yolov8.png",padded_image)




"""
import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('model\\best_yolov8_text_detection.pt')

# Resmi yükle
image = cv2.imread('sample\\lastikseridi\\_47.png', cv2.IMREAD_UNCHANGED)

# Resmin boyutlarını al
h, w = image.shape[:2]
maxlen = max(h,w)
# Yükseklik eksikliği (6443'e ulaşmak için gereken piksel sayısı)
height_diff = maxlen - h

# Üst ve alt siyah boşluklar için miktar
top_padding = height_diff // 2
bottom_padding = height_diff - top_padding  # Kalanı alta ekle

# Siyah padding ekleyerek 6443x6443 boyutlarına ulaştır
padded_image = cv2.copyMakeBorder(image, 0, bottom_padding, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])

results = model(padded_image)

for result in results[0].boxes:  # results[0] üzerinde çalış
    bbox = result.xyxy[0].cpu().numpy()  # Bounding box koordinatları (x1, y1, x2, y2)
    x1, y1, x2, y2 = map(int, bbox)  # Koordinatları tam sayıya çevir
    cv2.rectangle(padded_image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Bounding box çiz (yeşil renk)

cv2.imwrite("yontem3_yolov8.png",padded_image)
"""
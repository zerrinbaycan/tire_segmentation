import cv2
import numpy as np
from arducam_mipicamera import ArducamCamera
from time import sleep

IMAGE_DIR = "images"  # Resimlerin kaydedileceği klasör

def initialize_camera():
    """
    Kamerayı başlatır ve gerekli ayarları yapar.
    """
    print("Kamera başlatılıyor...")
    camera = ArducamCamera()
    camera.init_camera()  # Kamera başlatma
    camera.set_resolution(1920, 1080)  # Çözünürlük ayarı
    print("Kamera hazır!")
    return camera

def capture_image(camera):
    """
    Kameradan bir görüntü alır ve OpenCV formatında döndürür.
    """
    print("Resim çekiliyor...")
    frame = camera.capture()
    if frame is None:
        print("Resim alınamadı!")
        return None
    
    # Çerçeveyi OpenCV formatına dönüştür
    image = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
    return image

def save_image(image, file_name):
    """
    Görüntüyü PNG formatında kaydeder.
    """
    output_path = f"{IMAGE_DIR}/{file_name}"
    cv2.imwrite(output_path, image)
    print(f"Resim kaydedildi: {output_path}")

def main():
    # Resim kaydetme klasörünü oluştur
    import os
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    # Kamerayı başlat
    camera = initialize_camera()

    try:
        # Resim çek ve kaydet
        image = capture_image(camera)
        if image is not None:
            save_image(image, "captured_image.png")
    finally:
        # Kaynakları serbest bırak
        camera.close_camera()
        print("Kamera kapatıldı.")

if __name__ == "__main__":
    main()

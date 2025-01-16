import cv2
import os

# AVI dosyasını okuyup her bir frame'i PNG olarak kaydeden fonksiyon
def save_frames_from_avi(avi_file, output_folder):
    # Çıkış klasörünü oluşturun
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # AVI dosyasını açın
    cap = cv2.VideoCapture(avi_file)
    
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Mevcut frame'i PNG dosyası olarak kaydedin
        cv2.imwrite(os.path.join(output_folder, f'{frame_count}.png'), frame)
        frame_count += 1
    
    # Video capture nesnesini serbest bırakın
    cap.release()

# AVI dosyasının yolu
avi_file = 'C:\\Users\\Zerrin Baycan\\Desktop\\otput.avi'

if os.path.exists(avi_file):
    print("Dosya bulundu.")
else:
    print("Dosya yolu yanlış veya dosya mevcut değil.")

save_frames_from_avi(avi_file,'C:\\ZerrinGit\\tire_segmentation\\resimler')

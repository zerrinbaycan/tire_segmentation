import cv2
import numpy as np
import os
import time

# Klasörden resimleri okuyup tek bir array'e dönüştüren fonksiyon
def read_images_from_folder(folder_path):
    images = []
    filenames = sorted(os.listdir(folder_path), key=lambda x: int(os.path.splitext(x)[0]))
    for filename in filenames:
        img = cv2.imread(os.path.join(folder_path, filename))
        if img is not None:
            images.append(img)
    return np.array(images)

# Resimleri PNG dosyaları olarak kaydeden fonksiyon
def save_images_as_png(images, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for i, img in enumerate(images):
        cv2.imwrite(os.path.join(output_folder, f'image_{i}.png'), img)



# Resimleri AVI video dosyası olarak kaydeden fonksiyon
def save_images_as_avi(images, output_file):
    height, width, layers = images[0].shape
    video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'DIVX'), 1, (width, height))
    for img in images:
        video.write(img)
    video.release()

# Klasör yolunu belirtin
folder_path = 'C:\\ZerrinGit\\tire_segmentation\\evolog\\2024_11_15_160136'

# Resimleri klasörden okuyun
images = read_images_from_folder(folder_path)

# Resimleri PNG dosyaları olarak kaydetme süresini ölçün
start_time = time.time()
save_images_as_png(images, 'output_png')
png_time = time.time() - start_time

# Resimleri AVI dosyası olarak kaydetme süresini ölçün
start_time = time.time()
save_images_as_avi(images, 'C:\\ZerrinGit\\tire_segmentation\\evolog\\output.avi')
avi_time = time.time() - start_time

print(f"PNG olarak kaydetme süresi: {png_time} saniye")
print(f"AVI olarak kaydetme süresi: {avi_time} saniye")
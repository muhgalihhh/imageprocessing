import cv2
import numpy as np


def threshold(image, thresh=127, max_val=255, type_threshold=cv2.THRESH_BINARY):
    # Mengonversi gambar menjadi grayscale jika gambar memiliki lebih dari satu saluran warna
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
        
    # Menerapkan threshold pada gambar grayscale
    _, thresh_img = cv2.threshold(gray, thresh, max_val, type_threshold)
    return thresh_img

def adaptive_threshold(image, max_val=255, adaptive_method=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                      threshold_type=cv2.THRESH_BINARY, block_size=11, C=2):
    # Mengonversi gambar menjadi grayscale jika gambar memiliki lebih dari satu saluran warna
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
        
    # Memastikan block_size adalah angka ganjil
    if block_size % 2 == 0:
        block_size += 1
        
    # Menerapkan adaptive threshold pada gambar
    return cv2.adaptiveThreshold(gray, max_val, adaptive_method, threshold_type, block_size, C)

def otsu_threshold(image, max_val=255, threshold_type=cv2.THRESH_BINARY + cv2.THRESH_OTSU):
    # Mengonversi gambar menjadi grayscale jika gambar memiliki lebih dari satu saluran warna
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
        
    # Menerapkan Otsu's thresholding
    ret, thresh_img = cv2.threshold(gray, 0, max_val, threshold_type)
    return thresh_img, ret

def watershed_segmentation(image):
    # Mengonversi gambar menjadi grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Menerapkan threshold untuk memisahkan objek dari latar belakang
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Menghilangkan noise menggunakan operasi morfologi pembukaan
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # Area latar belakang pasti
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    
    # Menemukan area foreground yang pasti
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    
    # Menemukan area yang tidak diketahui
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # Labeling marker
    ret, markers = cv2.connectedComponents(sure_fg)
    
    # Menambahkan satu pada semua label agar latar belakang pasti tidak bernilai 0, tetapi 1
    markers = markers + 1
    
    # Menandai wilayah yang tidak diketahui dengan nol
    markers[unknown == 255] = 0
    
    # Menerapkan watershed
    markers = cv2.watershed(image, markers)
    
    # Mewarnai batasan watershed dengan warna merah
    image[markers == -1] = [0, 0, 255]  # Menandai batasan watershed dengan warna merah
    
    return image, markers

def k_means_segmentation(image, k=3, attempts=10):
    # Mengubah gambar menjadi array satu dimensi
    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    
    # Menentukan kriteria konvergensi untuk K-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    
    # Menerapkan algoritma K-means pada gambar
    _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, attempts, cv2.KMEANS_RANDOM_CENTERS)
    
    # Mengubah pusat kluster menjadi nilai integer
    centers = np.uint8(centers)
    
    # Mengambil label dan mengubah hasilnya kembali ke bentuk gambar
    labels = labels.flatten()
    segmented_image = centers[labels.flatten()]
    
    segmented_image = segmented_image.reshape(image.shape)
    
    return segmented_image, labels

def color_segmentation(image, lower_bound, upper_bound):
    # Membuat masker berdasarkan batas warna yang diberikan
    mask = cv2.inRange(image, lower_bound, upper_bound)
    
    # Mengambil hasil segmentasi berdasarkan masker
    result = cv2.bitwise_and(image, image, mask=mask)
    
    return result, mask

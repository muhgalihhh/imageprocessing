import cv2
import numpy as np


def apply_vintage_grunge(image):
    # Mengubah ukuran gambar menjadi 600x400
    image = cv2.resize(image, (600, 400))

    # 1. Terapkan filter sepia yang lebih kuat dengan tone orange/coklat
    # Sepia filter yang lebih warm dengan emphasis pada orange
    sepia_filter = np.array([[0.272, 0.534, 0.131],  # Blue channel - lebih sedikit
                             [0.349, 0.686, 0.168],  # Green channel
                             [0.393, 0.769, 0.189]]) # Red channel - lebih banyak
    sepia = cv2.transform(image, sepia_filter)
    sepia = np.clip(sepia, 0, 255).astype(np.uint8)

    # 2. Tambahkan warm overlay untuk meningkatkan tone orange
    warm_overlay = np.full_like(sepia, [20, 80, 120], dtype=np.uint8)  # BGR: lebih banyak red/yellow
    warm_sepia = cv2.addWeighted(sepia, 0.8, warm_overlay, 0.2, 0)

    # 3. Kurangi kontras dan terapkan blur ringan
    blur = cv2.GaussianBlur(warm_sepia, (3, 3), 0)
    faded = cv2.addWeighted(warm_sepia, 0.6, blur, 0.4, 0)

    # 4. Terapkan efek noise (grain) yang lebih vintage
    noise = np.random.normal(0, 15, faded.shape).astype(np.int16)
    noisy = np.clip(faded.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # 5. Tambahkan efek vignetting yang lebih dramatic
    rows, cols = noisy.shape[:2]
    center_x, center_y = cols // 2, rows // 2
    
    # Membuat masker vignetting dengan vectorized operation (lebih efisien)
    Y, X = np.ogrid[:rows, :cols]
    dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
    max_dist = np.sqrt(center_x**2 + center_y**2)
    
    # Vignetting yang lebih smooth dan dramatic
    vignette_mask = 1 - (dist_from_center / max_dist) * 0.7
    vignette_mask = np.clip(vignette_mask, 0.3, 1.0)  # Minimum brightness 30%
    
    # Apply vignetting ke setiap channel
    vignette = noisy.astype(np.float32)
    for i in range(3):
        vignette[:, :, i] *= vignette_mask
    vignette = np.clip(vignette, 0, 255).astype(np.uint8)

    # 6. Terapkan color grading vintage yang kuat - kurangi blue, tingkatkan red/yellow
    # Split channels untuk manipulasi individual
    b, g, r = cv2.split(vignette.astype(np.float32))
    
    # Kurangi blue channel secara signifikan
    b = b * 0.4
    
    # Tingkatkan red dan green untuk warm tone
    r = r * 1.4
    g = g * 1.1
    
    # Merge kembali
    vintage_image = cv2.merge([b, g, r])
    vintage_image = np.clip(vintage_image, 0, 255).astype(np.uint8)

    # 7. Tambahkan vintage color cast yang lebih kuat
    # Overlay warna orange/amber
    amber_overlay = np.full_like(vintage_image, [10, 60, 100], dtype=np.uint8)  # Amber color
    vintage_cast = cv2.addWeighted(vintage_image, 0.85, amber_overlay, 0.15, 0)

    # 8. Adjust exposure dan kontras untuk look vintage yang authentic
    # Sedikit overexpose untuk vintage look
    exposure_adjusted = cv2.convertScaleAbs(vintage_cast, alpha=1.1, beta=5)
    
    # Final contrast adjustment yang lebih soft
    final_result = cv2.convertScaleAbs(exposure_adjusted, alpha=1.2, beta=-15)

    # 9. Tambahkan sedikit desaturasi untuk vintage feel
    hsv = cv2.cvtColor(final_result, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = hsv[:, :, 1] * 0.7  # Kurangi saturasi
    final_vintage = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return final_vintage

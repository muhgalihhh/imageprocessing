import cv2
import numpy as np


def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def gaussian_blur(image, kernel_size=5):
    if kernel_size % 2 == 0:
        kernel_size += 1  # Ensure kernel size is odd
    
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def median_blur(image, kernel_size=5):
    if kernel_size % 2 == 0:
        kernel_size += 1  # Ensure kernel size is odd
        
    return cv2.medianBlur(image, kernel_size)

def bilateral_filter(image, d=9, sigma_color=75, sigma_space=75):
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)

def sobel_edge_detection(image, dx=1, dy=1, ksize=3):    
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
        
    sobel = cv2.Sobel(gray, cv2.CV_64F, dx, dy, ksize=ksize)
    abs_sobel = np.absolute(sobel)
    sobel_8u = np.uint8(255 * abs_sobel / np.max(abs_sobel))
    
    return sobel_8u

def canny_edge_detection(image, threshold1=100, threshold2=200):
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
        
    return cv2.Canny(gray, threshold1, threshold2)

def sharpen(image):
    kernel = np.array([[-1, -1, -1],
                      [-1,  9, -1],
                      [-1, -1, -1]])
    
    return cv2.filter2D(image, -1, kernel)

def emboss(image):
    kernel = np.array([[-2, -1, 0],
                      [-1,  1, 1],
                      [ 0,  1, 2]])
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
        
    return cv2.filter2D(gray, -1, kernel) + 128

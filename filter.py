import cv2
import numpy as np


def grayscale(image):
    """
    Convert image to grayscale
    
    Args:
        image: Input image in BGR format
        
    Returns:
        Grayscale image
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def gaussian_blur(image, kernel_size=5):
    """
    Apply Gaussian blur to an image
    
    Args:
        image: Input image
        kernel_size: Size of the Gaussian kernel (must be odd)
        
    Returns:
        Blurred image
    """
    if kernel_size % 2 == 0:
        kernel_size += 1  # Ensure kernel size is odd
    
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def median_blur(image, kernel_size=5):
    """
    Apply median blur to an image
    
    Args:
        image: Input image
        kernel_size: Size of the kernel (must be odd)
        
    Returns:
        Blurred image
    """
    if kernel_size % 2 == 0:
        kernel_size += 1  # Ensure kernel size is odd
        
    return cv2.medianBlur(image, kernel_size)

def bilateral_filter(image, d=9, sigma_color=75, sigma_space=75):
    """
    Apply bilateral filter to an image
    
    Args:
        image: Input image
        d: Diameter of each pixel neighborhood
        sigma_color: Filter sigma in the color space
        sigma_space: Filter sigma in the coordinate space
        
    Returns:
        Filtered image
    """
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)

def sobel_edge_detection(image, dx=1, dy=1, ksize=3):
    """
    Apply Sobel edge detection
    
    Args:
        image: Input grayscale image
        dx: Derivative order in x direction
        dy: Derivative order in y direction
        ksize: Size of the extended Sobel kernel
        
    Returns:
        Edge detected image
    """
    # Convert to grayscale if the image has more than one channel
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
        
    sobel = cv2.Sobel(gray, cv2.CV_64F, dx, dy, ksize=ksize)
    # Convert to absolute scale and then to 8-bit
    abs_sobel = np.absolute(sobel)
    sobel_8u = np.uint8(255 * abs_sobel / np.max(abs_sobel))
    
    return sobel_8u

def canny_edge_detection(image, threshold1=100, threshold2=200):
    """
    Apply Canny edge detection
    
    Args:
        image: Input grayscale image
        threshold1: First threshold for the hysteresis procedure
        threshold2: Second threshold for the hysteresis procedure
        
    Returns:
        Edge detected image
    """
    # Convert to grayscale if the image has more than one channel
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
        
    return cv2.Canny(gray, threshold1, threshold2)

def sharpen(image):
    """
    Sharpen an image
    
    Args:
        image: Input image
        
    Returns:
        Sharpened image
    """
    kernel = np.array([[-1, -1, -1],
                      [-1,  9, -1],
                      [-1, -1, -1]])
    
    return cv2.filter2D(image, -1, kernel)

def emboss(image):
    """
    Apply emboss effect to an image
    
    Args:
        image: Input image
        
    Returns:
        Embossed image
    """
    kernel = np.array([[-2, -1, 0],
                      [-1,  1, 1],
                      [ 0,  1, 2]])
    
    # Convert to grayscale if the image has more than one channel
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
        
    return cv2.filter2D(gray, -1, kernel) + 128

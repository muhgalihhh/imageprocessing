import cv2
import numpy as np


def threshold(image, thresh=127, max_val=255, type_threshold=cv2.THRESH_BINARY):
    """
    Apply thresholding to an image
    
    Args:
        image: Input grayscale image
        thresh: Threshold value
        max_val: Maximum value to use with binary thresholding types
        type_threshold: Thresholding type (cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV, etc.)
        
    Returns:
        Thresholded image
    """
    # Convert to grayscale if the image has more than one channel
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
        
    _, thresh_img = cv2.threshold(gray, thresh, max_val, type_threshold)
    return thresh_img

def adaptive_threshold(image, max_val=255, adaptive_method=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                      threshold_type=cv2.THRESH_BINARY, block_size=11, C=2):
    """
    Apply adaptive thresholding to an image
    
    Args:
        image: Input grayscale image
        max_val: Maximum value to use with binary thresholding types
        adaptive_method: Adaptive thresholding method
        threshold_type: Thresholding type
        block_size: Size of a pixel neighborhood that is used to calculate a threshold value
        C: Constant subtracted from the mean or weighted mean
        
    Returns:
        Adaptively thresholded image
    """
    # Convert to grayscale if the image has more than one channel
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
        
    # Ensure block_size is odd
    if block_size % 2 == 0:
        block_size += 1
        
    return cv2.adaptiveThreshold(gray, max_val, adaptive_method, threshold_type, block_size, C)

def otsu_threshold(image, max_val=255, threshold_type=cv2.THRESH_BINARY + cv2.THRESH_OTSU):
    """
    Apply Otsu thresholding to an image
    
    Args:
        image: Input grayscale image
        max_val: Maximum value to use with binary thresholding types
        threshold_type: Thresholding type
        
    Returns:
        Otsu thresholded image and optimal threshold value
    """
    # Convert to grayscale if the image has more than one channel
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
        
    ret, thresh_img = cv2.threshold(gray, 0, max_val, threshold_type)
    return thresh_img, ret

def watershed_segmentation(image):
    """
    Apply watershed segmentation
    
    Args:
        image: Input image (BGR format)
        
    Returns:
        Segmented image with different regions marked
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Noise removal using morphological opening
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # Sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)
    
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1
    
    # Mark the region of unknown with zero
    markers[unknown == 255] = 0
    
    # Apply watershed
    markers = cv2.watershed(image, markers)
    
    # Color the boundaries
    image[markers == -1] = [0, 0, 255]  # Mark watershed boundaries in red
    
    return image, markers

def k_means_segmentation(image, k=3, attempts=10):
    """
    Segment image using K-means clustering
    
    Args:
        image: Input image
        k: Number of clusters
        attempts: Number of times the algorithm is executed
        
    Returns:
        Segmented image and labels
    """
    # Reshape the image to a 2D array of pixels and 3 color values (RGB)
    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    
    # Define criteria and apply K-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, attempts, cv2.KMEANS_RANDOM_CENTERS)
    
    # Convert back to 8-bit values
    centers = np.uint8(centers)
    
    # Flatten the labels array
    labels = labels.flatten()
    
    # Convert all pixels to the color of the centroids
    segmented_image = centers[labels.flatten()]
    
    # Reshape back to the original image dimension
    segmented_image = segmented_image.reshape(image.shape)
    
    return segmented_image, labels

def color_segmentation(image, lower_bound, upper_bound):
    """
    Segment image based on color range
    
    Args:
        image: Input image (BGR format)
        lower_bound: Lower bound of color range (BGR)
        upper_bound: Upper bound of color range (BGR)
        
    Returns:
        Mask showing pixels within the specified color range
    """
    # Create a mask for the specified color range
    mask = cv2.inRange(image, lower_bound, upper_bound)
    
    # Apply the mask to the original image
    result = cv2.bitwise_and(image, image, mask=mask)
    
    return result, mask
